# E-Commerce Microservices Platform

A complete microservices-based e-commerce application built with Docker and Kubernetes, featuring user management, product catalog, shopping cart, and order processing.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Running with Docker Compose](#running-with-docker-compose)
- [Deploying to Kubernetes](#deploying-to-kubernetes)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Project Overview

This project demonstrates a production-ready microservices architecture with:

- **4 Independent Microservices**: Users, Products, Cart, Orders
- **Polyglot Persistence**: PostgreSQL for relational data, MongoDB for document storage
- **Containerization**: Docker and Docker Compose
- **Orchestration**: Kubernetes deployment with Minikube
- **Service Communication**: RESTful APIs with inter-service HTTP calls
- **Auto-scaling**: Horizontal Pod Autoscaler (HPA)
- **Health Monitoring**: Liveness and readiness probes

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│                  (Web/Mobile Applications)                  │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
               ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Users   │   │ Products │   │   Cart   │
        │ Service  │   │ Service  │   │ Service  │
        │  :8001   │   │  :8002   │   │  :8003   │
        └────┬─────┘   └─────┬────┘   └────┬─────┘
             │               │              │
             │               │              │
             ▼               ▼              │
        ┌─────────────────────┐            │
        │    PostgreSQL       │            │
        │  - users DB         │            │
        │  - products DB      │            │
        └─────────────────────┘            │
                                           │
        ┌──────────────────────────┐       │
        │    Orders Service        │◄──────┘
        │       :8004              │
        └──────────┬───────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │      MongoDB        │
        │  - cart DB          │
        │  - orders DB        │
        └─────────────────────┘
```

### Service Communication Flow

1. **Cart Service** validates users and products before cart operations
2. **Orders Service** coordinates with Cart, Users, and Products for order creation
3. All services use **Kubernetes DNS** for service discovery
4. **Health checks** ensure service availability

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## 💻 Technology Stack

### Backend Services
- **Python Services** (Users, Products):
  - FastAPI
  - SQLAlchemy (ORM)
  - asyncpg (PostgreSQL driver)
  - Pydantic (validation)

- **TypeScript/Node.js Services** (Cart, Orders):
  - Express.js
  - Mongoose (MongoDB ODM)
  - TypeScript for type safety

### Databases
- **PostgreSQL 17.5**: Relational data (Users, Products)
- **MongoDB 8.0**: Document storage (Cart, Orders)

### Infrastructure
- **Docker**: Containerization with multistage builds
- **Docker Compose**: Local multi-container orchestration
- **Kubernetes**: Production-grade orchestration
- **Minikube**: Local Kubernetes cluster

## 📦 Prerequisites

### Required Software
- Docker (v20.10+)
- Docker Compose (v2.0+)
- Minikube (latest)
- kubectl (latest)
- Node.js (v20+) - for local development
- Python (v3.11+) - for local development

### System Requirements
- 8GB RAM minimum
- 4 CPU cores recommended
- 20GB free disk space

### Installation Guides

**Docker:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# macOS
brew install docker
```

**Minikube:**
```bash
# Ubuntu/Debian
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS
brew install minikube
```

**kubectl:**
```bash
# Ubuntu/Debian
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Development)
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd microservices

# 2. Start all services
docker-compose up --build

# 3. Access services
# Users:    http://localhost:8001
# Products: http://localhost:8002
# Cart:     http://localhost:8003
# Orders:   http://localhost:8004
```

### Option 2: Kubernetes (Recommended for Production Testing)
```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker
minikube addons enable metrics-server

# 2. Build images for Kubernetes
eval $(minikube docker-env)
./setup_containers.sh

# 3. Deploy to Kubernetes
cd infra/scripts
./deploy.sh

# 4. Get service URLs
minikube service users -n ecommerce --url
minikube service products -n ecommerce --url
minikube service cart -n ecommerce --url
minikube service orders -n ecommerce --url
```

## 📁 Project Structure
```
microservices/
├── services/                    # Microservice implementations
│   ├── users/                  # User service (Python/FastAPI)
│   │   ├── app/
│   │   │   ├── core/          # Config, auth, security
│   │   │   ├── db/            # Database session
│   │   │   ├── models/        # SQLAlchemy models
│   │   │   ├── routers/       # API endpoints
│   │   │   ├── schemas/       # Pydantic schemas
│   │   │   ├── services/      # Business logic
│   │   │   └── main.py        # FastAPI app
│   │   └── requirements.txt
│   │
│   ├── products/               # Products service (Python/FastAPI)
│   │   ├── app/               # Similar structure to users
│   │   └── requirements.txt
│   │
│   ├── cart/                   # Cart service (TypeScript/Express)
│   │   ├── src/
│   │   │   ├── cart/          # Cart routes
│   │   │   ├── client/        # HTTP clients for other services
│   │   │   ├── db/            # MongoDB connection & schemas
│   │   │   ├── services/      # Business logic
│   │   │   └── utils/         # Logging utilities
│   │   ├── server.ts          # Express server
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── orders/                 # Orders service (TypeScript/Express)
│       ├── src/               # Similar structure to cart
│       ├── server.ts
│       ├── package.json
│       └── tsconfig.json
│
├── infra/                      # Infrastructure configuration
│   ├── dockerfiles/           # Multistage Dockerfiles
│   │   ├── Dockerfile.users
│   │   ├── Dockerfile.products
│   │   ├── Dockerfile.cart
│   │   └── Dockerfile.orders
│   │
│   ├── k8s/                   # Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── secrets/          # Kubernetes secrets
│   │   ├── configs/          # ConfigMaps
│   │   ├── databases/        # Database deployments
│   │   ├── services/         # Service deployments
│   │   ├── hpa/              # Horizontal Pod Autoscalers
│   │   └── network-policies/ # Network security policies
│   │
│   ├── db/                    # Database initialization
│   │   └── init.sql
│   │
│   └── scripts/               # Deployment scripts
│       ├── deploy.sh         # Deploy to Kubernetes
│       ├── cleanup.sh        # Clean up resources
│       └── test-k8s.sh       # Test K8s deployment
│
├── docker-compose.yml         # Docker Compose configuration
├── setup_containers.sh        # Build Docker images
├── README.md                  # This file
├── ARCHITECTURE.md            # Detailed architecture docs
├── TESTING.md                 # Testing guide
└── SETUP_CHECKLIST.md         # Implementation checklist
```

## 🐳 Running with Docker Compose

### Start Services
```bash
# Start all services in foreground
docker-compose up

# Start all services in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f users
```

### Test Services
```bash
# Health checks
curl http://localhost:8001/health  # Users
curl http://localhost:8002/health  # Products
curl http://localhost:8003/health  # Cart
curl http://localhost:8004/health  # Orders

# Register a user
curl -X POST http://localhost:8001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'

# Create a product
curl -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "stock": 50,
    "category": "Electronics"
  }'
```

### Stop Services
```bash
# Stop services (keeps data)
docker-compose down

# Stop and remove volumes (clears data)
docker-compose down -v
```

## ☸️ Deploying to Kubernetes

### Initial Setup
```bash
# 1. Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Enable metrics server (required for HPA)
minikube addons enable metrics-server

# 3. Verify cluster
kubectl cluster-info
kubectl get nodes
```

### Build and Deploy
```bash
# 1. Point Docker to Minikube's daemon
eval $(minikube docker-env)

# 2. Build all images
docker build -t ecommerce/users:latest \
  -f infra/dockerfiles/Dockerfile.users .
docker build -t ecommerce/products:latest \
  -f infra/dockerfiles/Dockerfile.products .
docker build -t ecommerce/cart:latest \
  -f infra/dockerfiles/Dockerfile.cart .
docker build -t ecommerce/orders:latest \
  -f infra/dockerfiles/Dockerfile.orders .

# 3. Deploy to Kubernetes
cd infra/scripts
chmod +x deploy.sh
./deploy.sh

# 4. Check deployment status
kubectl get all -n ecommerce

# 5. Get service URLs
minikube service users -n ecommerce --url
minikube service products -n ecommerce --url
minikube service cart -n ecommerce --url
minikube service orders -n ecommerce --url
```

### Monitor Deployment
```bash
# Watch pods start
kubectl get pods -n ecommerce -w

# Check pod logs
kubectl logs -n ecommerce -l app=users
kubectl logs -n ecommerce -l app=products

# Check HPA status
kubectl get hpa -n ecommerce

# Describe a pod for debugging
kubectl describe pod -n ecommerce <pod-name>
```

### Access Services
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Services are available at:
# Users:    http://$MINIKUBE_IP:30001
# Products: http://$MINIKUBE_IP:30002
# Cart:     http://$MINIKUBE_IP:30003
# Orders:   http://$MINIKUBE_IP:30004

# Or use minikube service command
minikube service users -n ecommerce
```

### Clean Up
```bash
# Remove all Kubernetes resources
cd infra/scripts
./cleanup.sh

# Or manually
kubectl delete namespace ecommerce

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## 📚 API Documentation

### Users Service (Port 8001/30001)

**Register User**
```bash
POST /api/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Login**
```bash
POST /api/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Get User Profile**
```bash
GET /api/users/{userId}
Authorization: Bearer {token}
```

### Products Service (Port 8002/30002)

**Get All Products**
```bash
GET /api/products
```

**Get Product by ID**
```bash
GET /api/products/{productId}
```

**Create Product**
```bash
POST /api/products
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 50,
  "category": "Electronics"
}
```

**Update Product Stock**
```bash
PUT /api/products/{productId}/stock
Content-Type: application/json

{
  "quantity": -5
}
```

### Cart Service (Port 8003/30003)

**Add Item to Cart**
```bash
POST /api/cart
Content-Type: application/json

{
  "userId": "user-id",
  "productId": "product-id",
  "quantity": 2
}
```

**Get User's Cart**
```bash
GET /api/cart/{userId}
```

**Update Cart Item**
```bash
PUT /api/cart/{userId}/items/{productId}
Content-Type: application/json

{
  "quantity": 3
}
```

**Remove from Cart**
```bash
DELETE /api/cart/{userId}/items/{productId}
```

### Orders Service (Port 8004/30004)

**Create Order**
```bash
POST /api/orders
Content-Type: application/json

{
  "userId": "user-id",
  "shippingAddress": {
    "street": "123 Main St",
    "city": "Toronto",
    "postalCode": "M5H 2N2",
    "country": "Canada"
  },
  "paymentMethod": "credit_card"
}
```

**Get User's Orders**
```bash
GET /api/orders/user/{userId}
```

**Get Order by ID**
```bash
GET /api/orders/{orderId}
```

**Update Order Status**
```bash
PUT /api/orders/{orderId}/status
Content-Type: application/json

{
  "status": "shipped"
}
```

## 🧪 Testing

See [TESTING.md](TESTING.md) for comprehensive testing guide.

### Quick Test
```bash
# For Docker Compose
curl http://localhost:8001/health

# For Kubernetes
cd infra/scripts
./test-k8s.sh
```

### Complete Integration Test
```bash
# 1. Register user
USER_RESPONSE=$(curl -X POST http://localhost:8001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!","name":"Test"}')

# 2. Create product
PRODUCT_RESPONSE=$(curl -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":999.99,"stock":100}')

# 3. Add to cart
curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{"userId":"'$USER_ID'","productId":"'$PRODUCT_ID'","quantity":1}'

# 4. Create order
curl -X POST http://localhost:8004/api/orders \
  -H "Content-Type: application/json" \
  -d '{"userId":"'$USER_ID'","shippingAddress":{...},"paymentMethod":"credit_card"}'
```

## 🐛 Troubleshooting

### Docker Compose Issues

**Services won't start:**
```bash
# Check logs
docker-compose logs [service-name]

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

**Database connection issues:**
```bash
# Check if databases are running
docker-compose ps postgres mongo

# Verify network
docker network ls
docker network inspect microservices_backend
```

### Kubernetes Issues

**Pods not starting:**
```bash
# Check pod status
kubectl get pods -n ecommerce

# Check pod events
kubectl describe pod -n ecommerce <pod-name>

# Check logs
kubectl logs -n ecommerce <pod-name>
```

**Images not found:**
```bash
# Verify you're using Minikube's Docker
eval $(minikube docker-env)

# Check images exist
docker images | grep ecommerce

# Rebuild if needed
docker build -t ecommerce/users:latest \
  -f infra/dockerfiles/Dockerfile.users .
```

**Services not accessible:**
```bash
# Check services
kubectl get svc -n ecommerce

# Get service URL
minikube service users -n ecommerce --url

# Check Minikube IP
minikube ip
```

**HPA not working:**
```bash
# Check if metrics-server is enabled
minikube addons list | grep metrics-server

# Enable if needed
minikube addons enable metrics-server

# Check HPA status
kubectl get hpa -n ecommerce
kubectl describe hpa users-hpa -n ecommerce
```

### Common Errors

**"Cannot connect to Docker daemon"**
```bash
# Start Docker service
sudo systemctl start docker

# Or start Docker Desktop (macOS/Windows)
```

**"Port already in use"**
```bash
# Find process using port
sudo lsof -i :8001

# Kill process
kill -9 <PID>
```

**"Out of memory" / "Resource exhausted"**
```bash
# Increase Docker resources in Docker Desktop settings
# Or for Minikube:
minikube delete
minikube start --cpus=4 --memory=8192
```

## 🔐 Security Notes

- **Development Only**: Current secrets are for development only
- **Change Passwords**: Always change default passwords in production
- **Use Secret Management**: In production, use Vault, AWS Secrets Manager, etc.
- **Enable TLS**: Use HTTPS/TLS for all communication in production
- **Network Policies**: Enable network policies in Kubernetes
- **RBAC**: Implement role-based access control

## 📖 Additional Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture and design decisions
- [TESTING.md](TESTING.md) - Comprehensive testing guide
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Implementation checklist

## 👥 Team Members

- Sagar Thapa
- Sachit Jaswal

## 📝 License

This project is for educational purposes as part of a Microservices Architecture course.

## 🤝 Contributing

This is a course project. For questions or issues, contact the project team members.

## 📧 Support

For help with this project:
1. Check [TROUBLESHOOTING](#troubleshooting) section
2. Review [TESTING.md](TESTING.md) for testing guidance
3. Contact team members via [your preferred communication channel]