pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Setup') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat '"%PYTHON%" -m pytest tests/'
            }
        }
        stage('Check Docker') {
            steps {
                bat 'docker --version'
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