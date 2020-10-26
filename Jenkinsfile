def project = 'electrum-vault'
def project_type = 'python'
def project_ext = 'bin'
def git_branch = env.BRANCH_NAME
def prefix_branch = env.BRANCH_NAME.replaceAll("/", "_")
def GitUrl = 'https://github.com/gostomski/'+project+'.git'
def gitCredentials ='jenkins-bitbucket-ssh'
def file_extension= '.txt'
def already_released_version=false
def force_release = false
def nexus_url = 'nexus.cloudbestenv.com:8443'



node('mac-jenkins') {

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        git url: GitUrl, branch: git_branch, credentialsId: gitCredentials
    }


    stage('build macos binary') {
        withEnv(["PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"]){
        sh '''
            git submodule update --init
            find contrib/osx/
            pushd contrib/osx/CalinsQRReader; xcodebuild; popd
            cp -r contrib/osx/CalinsQRReader/build prebuilt_qr
            ./contrib/osx/make_osx
           '''
        }
    }

    stage('Upload macos binary') {
        withEnv(["GIT_COMMITTER_NAME=Jenkins", "GIT_COMMITTER_EMAIL=jenkins@minebest.com"]) {
   
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        tag = sh(script: "git describe --tags --abbrev=9 --dirty --always",returnStdout:true,).trim()
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}.dmg", type: "dmg"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        
     }
    }

}
