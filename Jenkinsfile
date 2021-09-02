pipeline {
    agent none

    stages {
        stage('Build') {
            agent {
                docker { image 'python:3-alpine'}
            }
            steps {
                bat 'python -m venv env'
                bat 'call ./env/Scripts/activate.bat'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            agent {
                docker { image 'qnib/pytest'}
            }
            steps {
                bat 'mkdir -p ./allure-results'
                bat 'python -m pytest -v --reruns 2 --alluredir=./allure-results ./src/tests/'
            }
        }
        stage('reports') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
    }
}