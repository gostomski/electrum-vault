pipeline {
   agent {
        dockerfile {
            dir 'contrib/build-linux/appimage'
        }
   }
   stages {
        stage('Build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh './build.sh'
                }
            }
        }
   }
}

