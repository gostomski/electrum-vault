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
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        git url: GitUrl, branch: git_branch, credentialsId: gitCredentials
    }


    // stage('Build image') {
    //     /* This builds the actual image; synonymous to
    //      * docker build on the command line */

    //     app = docker.build("electrum-appimage-builder-cont","./contrib/build-linux/appimage")
    // }

    // stage('Release binary linux') {
    //      withEnv(["GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test"]) {
   
    //     /* Ideally, we would run a test framework against our image.
    //      * For this example, we're using a Volkswagen-type approach ;-) */

    //     app.inside {
    //         sh 'cd contrib/build-linux/appimage && ./build.sh'
    //     }
    //     tag = sh(script: "git describe --tags --abbrev=7 --dirty --always",returnStdout:true,).trim()       
    //     nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}-x86_64.AppImage", type: "${project_ext}"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        

    //     //add information about git
    //     sh "echo $project,$tag,$prefix_branch,$shortCommit > $project-$prefix_branch-latest.txt"
    //    nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "${project}-${prefix_branch}-latest.txt", type: "txt"]], credentialsId: 'jenkins-rw-nexus', groupId: 'Global', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
    //  cleanWs();
    //  }
    // }

    stage('Build image wine') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("electrum-wine-builder-img","./contrib/build-wine")
    }

    stage('Release binary wine') {
         withEnv(["GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test","PYTHONIOENCODING=UTF-8","LC_ALL=C.UTF-8", "LANG=C.UTF-8"]) {
   
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        pwd = sh(script: "pwd",returnStdout:true,).trim()
        sh 'docker run --rm -t -u 0 -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/bin/docker -w /opt/wine64/drive_c/electrum/contrib/build-wine -v $(pwd):/opt/wine64/drive_c/electrum:rw electrum-wine-builder-img ./build.sh'

        tag = sh(script: "git describe --tags --abbrev=9 --dirty --always",returnStdout:true,).trim()      
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}-portable.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "dist/electrum-${tag}-setup.exe", type: "exe"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
        

        //add information about git
            sh "echo $project,$tag,$prefix_branch,$shortCommit > $project-$prefix_branch-latest.txt"
           nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "${project}-${prefix_branch}-latest.txt", type: "txt"]], credentialsId: 'jenkins-rw-nexus', groupId: 'Global', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${tag}"
       cleanWs();
     }
    }

}
