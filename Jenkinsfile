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

        


        stage('SonarQube Analysis') {
            steps {
                script {

                    def scannerExecutable = '/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonarqube-scanner/bin/sonar-scanner'

                    def sonarProjectKey = 'weza_challenge'
                    
                    withSonarQubeEnv(installationName: 'sonarqube-server') {
                        sh "${scannerExecutable} -Dsonar.projectKey=${sonarProjectKey}"
                    }
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

        stage('Snyk scan'){
            steps{
                script{
                    

                    snykSecurity severity: 'critical', snykInstallation: 'snyk', snykTokenId: 'snyk-cred', args: '--allow-missing'
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
