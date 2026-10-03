pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        DOCKER = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        COMPOSE = 'C:\\Users\\kunal\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe'
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
        stage('Build Docker Image') {
            steps {
                echo 'Building FoodExpress Docker image...'
                bat '"%DOCKER%" build -t foodexpress:latest .'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying FoodExpress...'
                bat '"%COMPOSE%" down'
                bat '"%COMPOSE%" up -d --build'
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