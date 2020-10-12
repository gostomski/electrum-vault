def project = 'electrum-vault'
def project_type = 'python'
def project_ext = 'bin'
def git_branch = env.BRANCH_NAME
def prefix_branch = env.BRANCH_NAME.replaceAll("/", "_")
def shortCommit = ''
def GitUrl = 'https://github.com/gostomski/'+project+'.git'
def gitCredentials ='jenkins-bitbucket-ssh'
def file_extension= '.txt'
def already_released_version=false
def force_release = false
def nexus_url = 'nexus.cloudbestenv.com:8443'

node('local-docker') {
    def docker_linux
    def docker_wine

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        git url: GitUrl, branch: git_branch, credentialsId: gitCredentials
    }

    stage('Build image wine') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        sh 'sudo chown -R jenkins ./contrib/build-wine'
        sh 'ls -la ./contrib/build-wine'
        docker_wine = docker.build("electrum-wine-builder-img","./contrib/build-wine")
    }

}
