pipeline {
    agent {
        dockerfile {
            dir 'contrib/build-linux/appimage'
        }
    }    


   stages {
         stage('Initialize')  {         
            def dockerHome = tool 'myDocker'
            env.PATH = "${dockerHome}/bin:${env.PATH}"     
         } 
         stage('Build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh './build.sh'
                }
            }
        }
   }
}

