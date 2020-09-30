pipeline {
    agent {
        dockerfile {
            dir 'contrib/build-linux/appimage'
        }
    }    


   stages {
         stage('Build') {
            steps {
                    sh './build.sh'
            }
        }
   }
}

