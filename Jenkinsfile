pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
	        docker {
	            image 'python:3-alpine' 
	        }
            }
            steps {
	        sh 'python3 -m py_compile main.py gpcharts.py' 
	    }
        }
        stage("SonarQube") {
            agent any
            environment {
                scannerHome = tool 'SonarQube Scanner'
            }
            steps {
                withSonarQubeEnv('sonarqube.keremyaldiz.com') {
                    sh '${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=recommender-systems -Dsonar.sources=. -Dsonar.projectName=RS -Dsonar.projectVersion=0.1'
                }
            }
        }
        stage('Deliver') {
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python3'
                }
            }
            steps {
                sh 'pyinstaller --onefile main.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/main'
                }
            }
        }
    }
}
