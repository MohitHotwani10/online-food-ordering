pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        DOCKER = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
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
                bat '"%DOCKER%" --version'
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