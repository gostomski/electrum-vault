pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            label 'docker' 
            dir 'contrib/build-linux/appimage'
            args '-v $PWD:/opt/electrum'
        }
    }    


   stages {
        stage('Build') {
          agent {
                docker {
                filename 'Dockerfile'
                label 'docker' 
                dir 'contrib/build-linux/appimage'
                args '-v $PWD:/opt/electrum'
                }
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh './build.sh'
                }
            }
        }
   }
}

