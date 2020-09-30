node('local-docker') {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("electrum-appimage-builder-cont","./contrib/build-linux/appimage")
    }

    stage('Build binary') {
         withEnv(["GIT_COMMITTER_NAME=test", "GIT_COMMITTER_EMAIL=test"]) {
   
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside {
            sh 'pwd'
            sh 'ls -la'
            sh 'cd contrib/build-linux/appimage && ./build.sh'
        }
        sh 'ls -a dist/'
     }
    }

}
