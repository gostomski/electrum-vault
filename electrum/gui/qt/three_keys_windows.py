from datetime import datetime
from functools import partial

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QLineEdit, \
    QTreeView, QAbstractItemView, QHeaderView, QStyleOptionButton, QStyle

from .confirm_tx_dialog import ConfirmTxDialog
from .util import read_QIcon, WaitingDialog
from .main_window import ElectrumWindow
from electrum.i18n import _
from ... import bitcoin
from ...plugin import run_hook
from ...transaction import PartialTxOutput, PartialTxInput, PartialTransaction
from ...util import bfh


class CheckableHeader(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.parent = parent
        self.is_on = False

    def paintSection(self, painter: 'QPainter', rect: 'QRect', logical_index: int):
        painter.save()
        super().paintSection(painter, rect, logical_index)
        painter.restore()

        # assure set only in first column
        if logical_index == 0:
            option = QStyleOptionButton()
            option.rect = QRect(
                23, 3,
                14, 14
            )
            if self.is_on:
                option.state = QStyle.State_On
            else:
                option.state = QStyle.State_Off
            self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, option, painter)

    def mousePressEvent(self, event):
        if self.is_on:
            self.is_on = False
        else:
            self.is_on = True
        super().updateSection(0)
        super().mousePressEvent(event)


class TableItem(QStandardItem):
    def __init__(self, text, if_checkable=False):
        super().__init__(text)
        self.setCheckable(if_checkable)
        self.setTextAlignment(Qt.AlignRight)


class ElectrumARWindow(ElectrumWindow):
    LABELS = ['Date', 'Confirmation', 'Balance']

    def __init__(self, gui_object: 'ElectrumGui', wallet: 'Abstract_Wallet'):
        super().__init__(gui_object=gui_object, wallet=wallet)
        self.alert_transactions = []
        self.recovery_tab = self.create_recovery_tab()
        # todo add proper icon
        self.tabs.addTab(self.recovery_tab, read_QIcon("tab_send.png"), _('Recovery'))

    def create_recovery_tab(self):
        # todo finish development
        layout = QVBoxLayout()
        label = QLabel(_('Alert transaction to recovery'))
        layout.addWidget(label)

        self.view = QTreeView()
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        header = CheckableHeader(Qt.Horizontal, self.view)
        self.view.setHeader(header)
        self.view.setModel(self.model)
        self.view.setUniformRowHeights(True)
        self.model.setHorizontalHeaderLabels(self.LABELS)
        self.view.header().setDefaultAlignment(Qt.AlignRight)
        self.update_atx_table()

        layout.addWidget(self.view)

        hbox1 = QHBoxLayout()
        address_label = QLabel(_('Recovery address'))
        hbox1.addWidget(address_label)
        self.recovery_address_line = QLineEdit()
        hbox1.addWidget(self.recovery_address_line)

        hbox2 = QHBoxLayout()
        privkey_label = QLabel(_('Recovery private key'))
        hbox2.addWidget(privkey_label)
        self.recovery_privkey_line = QLineEdit()
        hbox2.addWidget(self.recovery_privkey_line)

        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

        widget = QWidget(parent=self)
        widget.setLayout(layout)

        update_button = QPushButton('Refresh transaction list')
        update_button.clicked.connect(self.update_atx_table)
        layout.addWidget(update_button)

        button = QPushButton('Recovery')
        button.clicked.connect(self.make_recovery)
        layout.addWidget(button)

        return widget

    def update_atx_table(self):
        self.alert_transactions = []
        self.model.removeRows(0, self.model.rowCount())
        for atx_info in self.wallet.get_atxs_to_recovery():
            self.alert_transactions.append(atx_info['transaction'])
            timestamp = atx_info['timestamp']
            str_datetime = ''
            if timestamp:
                str_datetime = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            self.model.appendRow([
                TableItem(str_datetime, if_checkable=True),
                TableItem(f"{atx_info['confirmations']: 3d}/144"),
                TableItem(f"{atx_info['balance'] / 100_000_000:.8f}"),
            ])

        for i in range(len(self.LABELS)):
            self.view.resizeColumnToContents(i)

    def _get_checked_atxs(self):
        return [self.alert_transactions[row]
                for row in range(self.model.rowCount()) if self.model.item(row, 0).checkState()]

    def _get_recovery_inputs_and_output(self, atxs, address):
        scriptpubkey = bfh(bitcoin.address_to_script(address))
        value = 0
        inputs = []
        for atx in atxs:
            for txout in atx.outputs():
                value += txout.value
            for txinp in atx.inputs():
                # todo check script witness flag !!!
                inputs.append(PartialTxInput.from_txin(txinp))
        return inputs, PartialTxOutput(scriptpubkey=scriptpubkey, value=value)

    def _get_recovery_keypair(self):
        recovery_pubkey = self.wallet.storage.get('recovery_pubkey')
        private_key = bytes.fromhex(self.recovery_privkey_line.text())
        return {recovery_pubkey: (private_key, True)}

    def make_recovery(self):
        address = self.recovery_address_line.text()
        recovery_keypair = self._get_recovery_keypair()
        print('++++ address ', address)
        atxs = self._get_checked_atxs()
        inputs, output = self._get_recovery_inputs_and_output(atxs, address)
        inputs = self.wallet.prepare_inputs_for_recovery(inputs)

        self.wallet.set_recovery()
        self.recovery_onchain_dialog(
            inputs=inputs,
            outputs=[output],
            recovery_keypairs=recovery_keypair,
        )

    def recovery_onchain_dialog(self, inputs, outputs, recovery_keypairs):
        """Code copied from pay_onchain_dialog"""
        external_keypairs = None
        invoice = None
        # trustedcoin requires this
        if run_hook('abort_send', self):
            return
        is_sweep = bool(external_keypairs)
        make_tx = lambda fee_est: self.wallet.make_unsigned_transaction(
            coins=inputs,
            outputs=outputs,
            fee=fee_est,
            is_sweep=is_sweep)
        if self.config.get('advanced_preview'):
            self.preview_tx_dialog(make_tx, outputs, external_keypairs=external_keypairs, invoice=invoice)
            return

        output_values = [x.value for x in outputs]
        output_value = '!' if '!' in output_values else sum(output_values)
        d = ConfirmTxDialog(self, make_tx, output_value, is_sweep)
        d.update_tx()
        if d.not_enough_funds:
            self.show_message(_('Not Enough Funds'))
            return
        cancelled, is_send, password, tx = d.run()
        if cancelled:
            return
        if is_send:
            def sign_done(success):
                if success:
                    self.broadcast_or_show(tx, invoice=invoice)
            self.sign_tx_with_password(tx, sign_done, password, recovery_keypairs)
        else:
            self.preview_tx_dialog(make_tx, outputs, external_keypairs=external_keypairs, invoice=invoice)

    def sign_tx_with_password(self, tx: PartialTransaction, callback, password, external_keypairs=None):
        def on_success(result):
            callback(True)
        def on_failure(exc_info):
            self.on_error(exc_info)
            callback(False)
        on_success = run_hook('tc_sign_wrapper', self.wallet, tx, on_success, on_failure) or on_success

        if external_keypairs and self.wallet.multisig_script_generator.is_recovery_mode():
            task = partial(self.wallet.sign_recovery_transaction, tx, password, external_keypairs)
        else:
            task = partial(self.wallet.sign_transaction, tx, password)
        msg = _('Signing transaction...')
        WaitingDialog(self, msg, task, on_success, on_failure)

    def sweep_key_dialog(self):
        self.wallet.set_alert()
        super().sweep_key_dialog()

    def pay_multiple_invoices(self, invoices):
        self.wallet.set_alert()
        super().pay_multiple_invoices(invoices)

    def do_pay_invoice(self, invoice):
        self.wallet.set_alert()
        super().do_pay_invoice(invoice)

    def show_recovery_tab(self):
        self.tabs.setCurrentIndex(self.tabs.indexOf(self.recovery_tab))
