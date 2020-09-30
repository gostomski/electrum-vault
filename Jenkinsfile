node('local-docker') {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("electrum-appimage-builder-cont","./contrib/build-linux/appimage")
    }

    stage('Build binary') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside("-w /opt/electrum/contrib/build-linux/appimage") {
            sh 'pwd'
        }
        app.inside {
            sh 'cd /opt/electrum/contrib/build-linux/appimage && ./build.sh'
        }
        sh 'ls -a dist/'
    }

}
