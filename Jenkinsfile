pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Setup') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest tests/'
            }
        }
    }

    post {
        success {
            echo 'FoodExpress CI Pipeline SUCCESS'
        }

        failure {
            echo 'FoodExpress CI Pipeline FAILED'
        }
    }
}