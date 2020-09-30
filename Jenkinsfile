pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'contrib/build-linux/appimage'
            args '-v $PWD:/opt/electrum'
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

