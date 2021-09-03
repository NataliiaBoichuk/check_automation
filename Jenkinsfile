pipeline {
    agent {
        docker { image 'python:3-alpine'}
    }

    stages {
        stage('Build') {
            steps {
                sh 'python -m venv env'
                sh 'source env/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'pip install chromedriver-binary'
            }
        }
        stage('Test') {
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