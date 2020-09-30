pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            label 'my-defined-label'
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

