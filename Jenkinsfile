properties([parameters([booleanParam(defaultValue: true, description: 'do not check last commit', name: 'force_release'),string(defaultValue: '0.0.1', description: 'release version', name: 'version', trim: false), string(defaultValue: 'master', description: 'branch for releases', name: 'branch', trim: false)])])

def last_commitid = ''
def project = 'electrum-vault'
def project_type = 'python'
def project_ext = 'bin'
def git_branch = branch
def prefix_branch = branch.replaceAll("/", "_")
def shortCommit = ''
def GitUrl = 'https://github.com/gostomski/'+project+'.git'
def gitCredentials ='jenkins-bitbucket-ssh'
def file_extension= '.txt'
def already_released_version=false
def force_release = false
def nexus_url = 'nexus.cloudbestenv.com:8443'

node('local-docker') {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        git url: GitUrl, branch: git_branch, credentialsId: gitCredentials
    }

    stage('Check last commit'){
      shortCommit = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%H'").trim()
      echo shortCommit
      //get recently release commit id
      if (force_release == 'false'){
        sh "wget --no-check-certificate https://${nexus_url}/repository/miningcityv2/Global/$project-$prefix_branch/$version/$project-$prefix_branch-$version$file_extension -O version.txt"
        last_commitid = sh(script: "cat version.txt | cut -f 4 -d ,",returnStdout:true,).trim()
        echo "Compare latest released commit $last_commitid to current commit id $shortCommit is ok"
        if (last_commitid != shortCommit){
           force_release = 'true'
           echo "FORCING RELEASE"
        }
        else {
            art_version = sh(script: "cat version.txt | cut -f 2 -d ,",returnStdout:true,).trim()
            already_released_version = true
        }
      }
    }
    if(already_released_version==true) {
       currentBuild.result = 'SUCCESS'
       echo "this commit was already released - use force release if you want to release"
     return
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("electrum-appimage-builder-cont","./contrib/build-linux/appimage")
    }

    stage('Build binary') {
         withEnv(["GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test"]) {
   
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside {
            sh 'pwd'
            sh 'ls -la'
            sh 'cd contrib/build-linux/appimage && ./build.sh'
        }
        tag = sh(script: "git describe --tags --abbrev=7 --dirty --always",returnStdout:true,).trim()      
        //echo prefix_branch
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}-x86_64.AppImage", type: "${project_ext}"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        

        //add information about git
        sh "echo $project,$tag,$prefix_branch,$shortCommit > $project-$prefix_branch-latest.txt"
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "${project}-${prefix_branch}-latest.txt", type: "txt"]], credentialsId: 'jenkins-rw-nexus', groupId: 'Global', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
     cleanWs();
     }
    }
    stage('Create package and upload'){
        
    }

}



