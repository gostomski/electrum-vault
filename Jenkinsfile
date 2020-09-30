def last_commitid = ''
def project = 'electrum-vault'
def project_type = 'python'
def project_ext = ''
//def git_branch = branch
def shortCommit = ''
def GitUrl = 'https://github.com/gostomski/'+project+'.git'
def gitCredentials ='jenkins-bitbucket-ssh'
def file_extension= '.txt'
def already_released_version=false
def force_release = false
def nexus_url = 'https://nexus.cloudbestenv.com:8443/'

node('local-docker') {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

    stage('Check last commit'){
      shortCommit = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%H'").trim()
      echo shortCommit
      //get recently release commit id
      if (force_release == 'false'){
        sh "wget --no-check-certificate https://${nexus_url}/repository/miningcityv2/Global/$project-$branch/$version/$project-$branch-$version$file_extension -O version.txt"
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
        tag = sh(script: "git describe --tags",returnStdout:true,).trim()

        //nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}-x86_64.AppImage", type: "${project_ext}"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${version}"
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "contrib/build-linux/README.md", type: "${project_ext}"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${version}"
        //add information about git
        sh "echo $project,$version,$branch,$shortCommit > $project-$branch-latest.txt"
        sh "echo $project,$version,$branch,$shortCommit"
        //nexusArtifactUploader artifacts: [[artifactId: "$project-$branch", classifier: '', file: "$project-$branch-latest.txt", type: "txt"]], credentialsId: 'jenkins-rw-nexus', groupId: 'Global', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${version}"
    cleanWs();
     }
    }
    stage('Create package and upload'){
        
    }

}

