# FoodExpress - Online Food Ordering System

FoodExpress is an Online Food Ordering System developed as an ASD&D mini project.

## Features

- User Registration and Login
- Secure Password Hashing
- Food Menu
- Shopping Cart
- Checkout
- Order History
- Order Status Tracking
- Admin Dashboard
- Food Management
- Order Management

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- HTML
- CSS
- Bootstrap
- SQLite

## DevOps Tools

This project demonstrates:

- Git and GitHub
- Docker
- Docker Compose
- Jenkins
- Jira
- Prometheus
- AWS
- Terraform

## 

Entering sql :
docker exec -it foodexpress-db mysql -ufooduser -pfoodpass foodexpress

##

ngrok used for tunnel between jenkins and github
to connect between github and jenkins
.\ngrok.exe http 8080

## jira

## pipeline
current pipeline for jenkins(CI/CD)
git push
   ↓
GitHub
   ↓ webhook
Jenkins starts automatically
   ↓
Tests
   ↓
Build Docker image
   ↓
Deploy stage
   ↓
docker-compose down
   ↓
docker-compose up -d --build
   ↓
foodexpress-db starts automatically
   ↓
MySQL becomes healthy
   ↓
foodexpress-web starts automatically

## Project

ASD&D Mini Project - Online Food Ordering System