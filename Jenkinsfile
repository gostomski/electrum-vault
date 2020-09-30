pipeline {
/*    agent {
        dockerfile {
            dir 'contrib/build-linux/appimage'
        }
    }    
*/

agent { docker { image 'python:3.6' } }

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

