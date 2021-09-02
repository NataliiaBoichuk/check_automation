pipeline {
    agent any

    stages {
        stage('Build') {
            agent {
                docker { image 'python:3-alpine'}
            }
            steps {
                sh 'python -m venv env'
                sh 'call ./env/Scripts/activate.bat'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            agent {
                docker { image 'qnib/pytest'}
            }
            steps {
                sh 'mkdir -p ./allure-results'
                sh 'python -m pytest -v --reruns 2 --alluredir=./allure-results ./src/tests/'
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