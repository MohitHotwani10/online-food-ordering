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
A Docker image is a read-only template containing our application and its dependencies, whereas a Docker container is a running instance of that image.

##
building docker compose
docker compose up -d --build

##
docker ps
        ↓
All running Docker containers
        ↓
foodexpress-web
foodexpress-db
foodexpress-prometheus


docker compose ps
        ↓
Containers belonging to THIS Compose project
        ↓
none

##
activating virtual environment
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

## 

Entering sql :
docker exec -it foodexpress-db mysql -ufooduser -pfoodpass foodexpress

##

to run single container
docker run -d -p 5000:5000 --name foodexpress-container foodexpress

##

ngrok used for tunnel between jenkins and github
to connect between github and jenkins
.\ngrok.exe http 8080

##
starting 
docker start foodexpress-web foodexpress-db foodexpress-prometheus

## jira

##

## docker
to stop docker
docker stop foodexpress-web foodexpress-db foodexpress-prometheus

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

## prometheus
to open prometheus
http://localhost:9090

/metrics = data produced by application
Prometheus = collects/stores monitoring data
PromQL query = asks questions about that data

queries
1-up
2-flask_http_request_total
3-flask_http_request_duration_seconds_count
4-flask_http_request_duration_seconds_sum
5-
flask_http_request_duration_seconds_sum
/
flask_http_request_duration_seconds_count

flask_http_request_total
        ↓
How many HTTP requests occurred

flask_http_request_duration_seconds_count
        ↓
How many requests were measured for duration

flask_http_request_duration_seconds_sum
        ↓
Total time spent processing those measured requests

_count → How many requests?
_sum   → How much total time?
_sum / _count → Average time per request

FoodExpress
    ↓
generates HTTP activity
    ↓
/metrics exposes metrics
    ↓
Prometheus scrapes web:5000 every 5 seconds
    ↓
PromQL query
    ↓
Request counts / errors / availability

200 → OK / Successful              ✅

302 → Redirect                     ↪️

304 → Not Modified / Use cache     📦

404 → Page/resource not found      ❌

500 → Internal server error        ❌

## Project

ASD&D Mini Project - Online Food Ordering System