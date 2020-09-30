def last_commitid = ''
def project = 'eectrum-api'
def project_type = 'pyhton'
def project_ext = 'bin'
def git_branch = branch
def shortCommit = ''
def nexus_url='nexus.cloudbestenv.com:8443'

pipeline {
    agent {
        // Equivalent to "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/
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

