pipeline {
   agent {
        dockerfile {
            dir 'contrib/build-linux/appimage'
        }
   }
   stages {
        stage('Build') {
            steps {
                withEnv(['HOME='+pwd()]) {
                    sh './build.sh'
                }
            }
        }

/*
    stage('Create package and upload'){
        
        sh "zip -9 -qr ${project}-${project_type}.${project_ext} ./ --exclude='.git/*'"
        nexusArtifactUploader artifacts: [[artifactId: "${project}-${project_type}", classifier: '', file: "${project}-${project_type}.${project_ext}", type: "${project_ext}"]], credentialsId: 'jenkins-rw-nexus', groupId: '', nexusUrl: "${nexus_url}", nexusVersion: 'nexus3', protocol: 'https', repository: 'miningcityv2', version: "${version}"
    cleanWs();
    }

*/
   }
}

