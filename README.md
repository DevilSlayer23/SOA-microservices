Ecommerce Microservices Project

This project uses a polyglot microservice setup:

FastAPI → Users + Products

Express.js → Cart + Orders

Postgres → FastAPI database

MongoDB → Express database

Docker Compose → Orchestration

Everything runs in containers.
Each service has its own environment file and Dockerfile.

1. Requirements

Install these first:

Docker

Docker Compose

(Optional) Node 20+ for local Express development

(Optional) Python 3.11+ for local FastAPI development

2. Project Structure
project/
  docker-compose.yml
  dockerfiles/
    Dockerfiles.fastapi
    Dockerfiles.express
  express_api/
    src/
    .env
    package.json
    .dockerignore
  fast_api/
    app/
    .env
    requirements.txt
    .dockerignore

3. Environment Variables
FastAPI .env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ecommerce_db
JWT_SECRET=your_secret

Express .env
MONGO_URI=mongodb://mongo:27017/ecommerce
JWT_SECRET=your_secret


Make sure these files exist before running Docker.

4. Start the Entire Stack

Run from project root:

docker compose build
docker compose up


This starts:

Postgres

MongoDB

FastAPI (http://localhost:8000
)

Express API (http://localhost:3000
)

View logs
docker compose logs fast_api
docker compose logs express_api

5. API Endpoints
FastAPI (Users + Products)

Base:

http://localhost:8000


Endpoints:

GET /health
POST /users/register
POST /users/login
GET /products
POST /products

Express API (Cart + Orders)

Base:

http://localhost:3000


Endpoints:

GET /health
GET /cart/:userId
POST /cart/add
POST /orders/checkout

6. Service-to-Service Communication

Inside Docker, services use service names, not localhost.

Express → FastAPI
http://fast_api:8000/products

FastAPI → Express
http://express_api:3000/cart/123


If you use localhost inside containers, the request will fail.

7. Reset Databases

If Postgres/Mongo get corrupted:

docker compose down -v
docker compose up --build


-v removes volumes → wipes all database data.

**8. Running Locally

(Optional – without Docker)**

FastAPI
cd fast_api
pip install -r requirements.txt
uvicorn app.main:app --reload

Express
cd express_api
npm install
npm run dev


Update env URLs to localhost when running locally.

9. Troubleshooting
FastAPI can't connect to Postgres

Your DATABASE_URL is wrong.
Must be:

postgresql://postgres:postgres@postgres:5432/ecommerce_db

Express can't connect to Mongo

Use:

mongodb://mongo:27017

curl “connection refused” in health checks

Service crashed. Check logs:

docker compose logs <service>

10. Stop All Containers
docker compose down
