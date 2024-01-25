pipeline{
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'weza_challenge.settings'
        GIT_REPO_NAME = determineRepoName()
        GIT_COMMIT = getCommit()
        TIME_STAMP = BUILDVERSION()
        DOCKERHUB_CREDENTIALS = credentials('sjmwatsefu-dockerhub')
    }

    stages{
        stage('Checkout') {
            steps{
                checkout scm
            }

        }

        stage('Check Scanner Location') {
            steps{
                script{
                    sh 'ls /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonarqube-scanner'
                }
            }
        }
      


        stage('SonarQube Analysis') {
            steps {
                script {

                    def scannerExecutable = '/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonarqube-scanner/bin/sonar-scanner'
                    
                    withSonarQubeEnv(installationName: 'sonarqube-server') {
                        sh "${scannerExecutable}"
                    }
                }
            }
        }

        stage('Run tests') {
            steps{
                script {
                    sh 'python manage.py test'
                }
            }

        }

        stage('Build docker image'){
            steps {
                script {
                    sh 'docker build -t sjmwatsefu/${GIT_REPO_NAME}:dev-${GIT_COMMIT}-${TIME_STAMP} .'
                }
            }
        }

        stage('Docker login'){
            steps {
                script {
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                }
            }
        }

        stage('Push image'){
            steps {
                script {
                    sh "docker push sjmwatsefu/${GIT_REPO_NAME}:dev-${GIT_COMMIT}-${TIME_STAMP}"
                }
            }
        }

    }
}

String determineRepoName() {
    return   GIT_URL.replaceFirst(/^.*\/([^\/]+?).git$/, '$1')
}

String getCommit(){
   return GIT_COMMIT[0..7]
}


def BUILDVERSION(){
    timestamp=Calendar.getInstance().getTime().format('YYYYMMddHHmmss',TimeZone.getTimeZone('EAT'))
    return timestamp
}
