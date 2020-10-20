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

node('mac-jenkins') {
    def docker_linux
    def docker_wine

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        git url: GitUrl, branch: git_branch, credentialsId: gitCredentials
    }



    stage('build macos binary') {
        sh '''
            #sudo xcode-select -s $HOME/Downloads/Xcode.app/Contents/Developer/
            git submodule update --init
            find contrib/osx/
            pushd contrib/osx/CalinsQRReader; xcodebuild; popd
            cp -r contrib/osx/CalinsQRReader/build prebuilt_qr
            ./contrib/osx/make_osx
            find dist/            
           '''
    }

    stage('Release binary wine') {
        withEnv(["GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test","PYTHONIOENCODING=UTF-8","LC_ALL=C.UTF-8", "LANG=C.UTF-8"]) {
   
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        pwd = sh(script: "pwd",returnStdout:true,).trim()
        sh 'pwd'
        tag = sh(script: "git describe --tags --abbrev=9 --dirty --always",returnStdout:true,).trim()
        sh 'find'      
        //nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "contrib/build-wine/dist/electrum-${tag}.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        //nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "contrib/build-wine/dist/electrum-${tag}-portable.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        //nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "contrib/build-wine/dist/electrum-${tag}-setup.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        

        //add information about git
        //sh "echo $project,$tag,$prefix_branch,$shortCommit > $project-$prefix_branch-latest.txt"
        //nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "${project}-${prefix_branch}-latest.txt", type: "txt"]], credentialsId: 'jenkins-rw-nexus', groupId: 'Global', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
       cleanWs();
     }
    }

}
