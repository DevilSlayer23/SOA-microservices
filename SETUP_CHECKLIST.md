# Project Setup Checklist

Complete implementation checklist for Part 1 of the Microservices Project.

## 📋 Pre-Implementation Checklist

### Environment Setup
- [ ] Docker installed (v20.10+)
- [ ] Docker Compose installed (v2.0+)
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Postman or similar API testing tool
- [ ] 4GB+ RAM available
- [ ] 10GB+ disk space available

### Project Structure Created
```
microservices/
├── services/
│   ├── users/
│   │   ├── app/
│   │   ├── requirements.txt
│   │   └── .env.prod
│   ├── products/
│   │   ├── app/
│   │   ├── requirements.txt
│   │   └── .env.prod
│   ├── cart/
│   │   ├── src/
│   │   ├── package.json
│   │   ├── server.js
│   │   └── .env.prod
│   └── orders/
│       ├── src/
│       ├── package.json
│       ├── server.js
│       └── .env.prod
├── infra/
│   ├── dockerfiles/
│   │   ├── Dockerfile.users
│   │   ├── Dockerfile.products
│   │   ├── Dockerfile.cart
│   │   └── Dockerfile.orders
│   └── db/
│       └── init.sql
├── docker-compose.yaml
├── README.md
├── API_DOCUMENTATION.md
├── ARCHITECTURE.md
└── TESTING.md
```

---

## 🔧 Implementation Steps

### Step 1: Set Up Databases

#### Create PostgreSQL Init Script

Create `infra/db/init.sql`:
```sql
-- Create databases
CREATE DATABASE ecommerce_users;
CREATE DATABASE ecommerce_products;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE ecommerce_users TO admin;
GRANT ALL PRIVILEGES ON DATABASE ecommerce_products TO admin;
```

- [ ] File created
- [ ] Syntax verified

#### Create Environment Files

**services/users/.env.prod**:
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=PassW0rd
POSTGRES_DB=ecommerce_users
DATABASE_URL=postgresql+asyncpg://admin:PassW0rd@postgres:5432/ecommerce_users
JWT_SECRET=your-super-secret-jwt-key-change-in-production
PROJECT_NAME=Users Service
PROJECT_VERSION=1.0.0
```

**services/products/.env.prod**:
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=PassW0rd
POSTGRES_DB=ecommerce_products
DATABASE_URL=postgresql+asyncpg://admin:PassW0rd@postgres:5432/ecommerce_products
PROJECT_NAME=Products Service
PROJECT_VERSION=1.0.0
```

**services/cart/.env.prod**:
```env
MONGO_URI=mongodb://mongo:27017/ecommerce_cart
USERS_SERVICE_URL=http://ecom_users:8001
PRODUCTS_SERVICE_URL=http://ecom_products:8002
PORT=8003
```

**services/orders/.env.prod**:
```env
MONGO_URI=mongodb://mongo:27017/ecommerce_orders
USERS_SERVICE_URL=http://ecom_users:8001
PRODUCTS_SERVICE_URL=http://ecom_products:8002
CART_SERVICE_URL=http://ecom_cart:8003
PORT=8004
```

- [ ] All .env.prod files created
- [ ] Credentials set
- [ ] Service URLs configured

### Step 2: Implement Python Services (Users & Products)

#### Users Service Files

**services/users/app/main.py** - Already provided in your code

**services/users/requirements.txt**:
```txt
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
asyncpg==0.29.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

- [ ] main.py implemented
- [ ] Health check endpoint works
- [ ] User registration endpoint implemented
- [ ] User login endpoint implemented
- [ ] JWT authentication working
- [ ] Database models created
- [ ] requirements.txt created

#### Products Service Files

Similar structure to Users service:
- [ ] main.py implemented
- [ ] Product CRUD endpoints
- [ ] Stock management endpoint
- [ ] Database models created
- [ ] requirements.txt created

### Step 3: Implement Node.js Services (Cart & Orders)

#### Cart Service Files

**services/cart/package.json**:
```json
{
  "name": "cart-service",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^8.0.3",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }
}
```

Files to create:
- [ ] server.js (main entry point)
- [ ] src/models/Cart.js (Mongoose model)
- [ ] src/routes/cart.js (API routes)
- [ ] src/services/externalServices.js (inter-service calls)
- [ ] src/config/database.js (MongoDB connection)
- [ ] package.json created

#### Orders Service Files

**services/orders/package.json**: Similar to cart service

Files to create:
- [ ] server.js (main entry point)
- [ ] src/models/Order.js (Mongoose model)
- [ ] src/routes/orders.js (API routes)
- [ ] src/services/externalServices.js (inter-service calls)
- [ ] src/config/database.js (MongoDB connection)
- [ ] package.json created

### Step 4: Create Multistage Dockerfiles

Using the Dockerfiles provided in the artifacts:

- [ ] infra/dockerfiles/Dockerfile.users created (multistage)
- [ ] infra/dockerfiles/Dockerfile.products created (multistage)
- [ ] infra/dockerfiles/Dockerfile.cart created (multistage)
- [ ] infra/dockerfiles/Dockerfile.orders created (multistage)
- [ ] All use non-root users
- [ ] All have curl installed for health checks
- [ ] Builder stages separate from runtime

### Step 5: Configure Docker Compose

Use the fixed docker-compose.yaml from artifacts:

- [ ] Relative paths (no absolute /home/... paths)
- [ ] MongoDB URIs use service names (mongo not 127.0.0.1)
- [ ] Health checks configured for all services
- [ ] start_period added to health checks (30-40s)
- [ ] Service dependencies properly set
- [ ] Networks configured
- [ ] Volumes for data persistence

### Step 6: Implement Inter-Service Communication

#### Cart Service
- [ ] verifyUser() function calls Users Service
- [ ] getProduct() function calls Products Service
- [ ] Stock validation before adding to cart
- [ ] Error handling for service failures

#### Orders Service
- [ ] verifyUser() function implemented
- [ ] getUserCart() function calls Cart Service
- [ ] verifyCartProducts() function calls Products Service
- [ ] updateProductStock() function calls Products Service
- [ ] clearUserCart() function calls Cart Service
- [ ] Transaction-like logic for order creation

### Step 7: Create Documentation

#### README.md
- [ ] Project overview
- [ ] Architecture diagram (ASCII or image)
- [ ] Service descriptions
- [ ] Technology stack listed
- [ ] Installation instructions
- [ ] Running instructions
- [ ] API endpoint list
- [ ] Database design explained
- [ ] Troubleshooting section

#### API_DOCUMENTATION.md
- [ ] All endpoints documented
- [ ] Request/response examples for each endpoint
- [ ] Error responses documented
- [ ] Authentication explained
- [ ] Query parameters documented

#### ARCHITECTURE.md
- [ ] High-level architecture diagram
- [ ] Service responsibilities explained
- [ ] Communication patterns documented
- [ ] Sequence diagrams for key flows:
  - [ ] User registration
  - [ ] Add to cart
  - [ ] Create order
- [ ] Database schema for each service
- [ ] Security architecture explained

#### TESTING.md
- [ ] Quick start testing guide
- [ ] Manual testing commands for all endpoints
- [ ] Integration test script
- [ ] Error scenario tests
- [ ] Debugging guide
- [ ] Test checklist

---

## ✅ Testing Checklist

### Build and Start
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

- [ ] All containers start without errors
- [ ] All containers show "healthy" status
- [ ] No error messages in logs

### Service Health Checks
- [ ] Users Service: `curl http://localhost:8001/health` returns 200
- [ ] Products Service: `curl http://localhost:8002/health` returns 200
- [ ] Cart Service: `curl http://localhost:8003/health` returns 200
- [ ] Orders Service: `curl http://localhost:8004/health` returns 200

### Functional Testing
- [ ] User registration works
- [ ] User login works and returns JWT
- [ ] Create products successfully
- [ ] Get all products works
- [ ] Get product by ID works
- [ ] Add item to cart works (verifies user and product)
- [ ] Get cart works
- [ ] Update cart quantity works
- [ ] Remove from cart works
- [ ] Create order from cart works
- [ ] Cart is cleared after order
- [ ] Product stock is updated after order
- [ ] Get user orders works
- [ ] Get order by ID works
- [ ] Update order status works
- [ ] Cancel order works and restores stock

### Error Handling Testing
- [ ] Invalid user returns 404
- [ ] Invalid product returns 404
- [ ] Insufficient stock returns 400
- [ ] Empty cart order returns 400
- [ ] Invalid credentials return 401

### Inter-Service Communication
- [ ] Cart validates user exists before adding items
- [ ] Cart validates product exists before adding items
- [ ] Cart checks product stock availability
- [ ] Orders validates user exists
- [ ] Orders gets cart from Cart Service
- [ ] Orders validates all products in cart
- [ ] Orders updates product stock
- [ ] Orders clears cart after creation

### Database Persistence
```bash
docker-compose restart
```
- [ ] Users persist after restart
- [ ] Products persist after restart
- [ ] Cart data persists after restart
- [ ] Orders persist after restart

---

## 📊 Rubric Self-Assessment

### Architecture and Design (4 points)

**Microservices Design (1 point)**:
- [ ] 4 modular services with distinct purposes
- [ ] RESTful API conventions followed
- [ ] Inter-service HTTP communication implemented
Score: ___/1

**Database Design (1 point)**:
- [ ] Separate databases per service
- [ ] Polyglot persistence (PostgreSQL + MongoDB)
Score: ___/1

**Service Discovery (0.5 points)**:
- [ ] Docker DNS for service discovery
- [ ] Service names used in environment variables
Score: ___/0.5

**Documentation (1.5 points)**:
- [ ] Architecture diagrams created
- [ ] Sequence diagrams for key flows
- [ ] Service interactions documented
- [ ] API endpoints documented
Score: ___/1.5

**Total Architecture**: ___/4

### Docker Implementation (3 points)

**Docker Images (1 point)**:
- [ ] Multistage builds implemented
- [ ] Lightweight images (slim/alpine)
- [ ] Optimized layer caching
Score: ___/1

**Docker Compose (1 point)**:
- [ ] Complete docker-compose.yaml
- [ ] All services configured
- [ ] Health checks implemented
- [ ] Dependencies properly set
Score: ___/1

**Security Best Practices (1 point)**:
- [ ] Non-root users in all containers
- [ ] Environment variables for secrets
- [ ] No hardcoded credentials
- [ ] Relative paths (no absolute paths)
Score: ___/1

**Total Docker**: ___/3

### **TOTAL PART 1**: ___/7

---

## 🚀 Submission Checklist

Before submitting Part 1:

### Code Repository
- [ ] All code committed to Git
- [ ] .gitignore configured (exclude .env files)
- [ ] README.md in root directory
- [ ] Clean commit history with meaningful messages

### Documentation
- [ ] README.md complete
- [ ] API_DOCUMENTATION.md complete
- [ ] ARCHITECTURE.md with diagrams complete
- [ ] TESTING.md complete

### Docker Files
- [ ] All Dockerfiles use multistage builds
- [ ] docker-compose.yaml has no absolute paths
- [ ] All environment variables in .env.prod files
- [ ] Health checks configured

### Testing
- [ ] Complete flow test passed
- [ ] All error scenarios tested
- [ ] Database persistence verified
- [ ] Inter-service communication verified

### Presentation Materials
- [ ] Architecture diagram (for presentation)
- [ ] Demo script prepared
- [ ] Screenshots of working system
- [ ] Video recording (optional but recommended)

---

## 📝 Common Issues and Solutions

### Issue: Container won't start
```bash
# Check logs
docker-compose logs [service_name]

# Common causes:
# - Syntax error in code
# - Missing dependency in requirements.txt/package.json
# - Wrong file paths in Dockerfile
# - Port already in use
```

### Issue: Health check failing
```bash
# Check if service is actually running
docker-compose exec [service_name] curl http://localhost:[port]/health

# Common causes:
# - Service not listening on 0.0.0.0
# - curl not installed in container
# - Database connection failing
# - Wrong port in health check
```

### Issue: Inter-service communication failing
```bash
# Check network
docker network ls
docker network inspect [network_name]

# Test connectivity
docker-compose exec cart ping ecom_users

# Common causes:
# - Wrong service name in URL
# - Service not healthy yet
# - Firewall blocking
```

### Issue: Database connection failing
```bash
# Check database logs
docker-compose logs postgres
docker-compose logs mongo

# Test connection
docker-compose exec postgres psql -U admin -d ecommerce_users

# Common causes:
# - Wrong credentials
# - Database not initialized
# - Wrong host (localhost vs service name)
```

---

## 🎯 Next Steps (Part 2)

After completing Part 1, prepare for Part 2:
- [ ] Research Kubernetes basics
- [ ] Install Minikube or Kind
- [ ] Learn kubectl commands
- [ ] Study Kubernetes resources (Pods, Services, Deployments)
- [ ] Research ConfigMaps and Secrets
- [ ] Learn about Horizontal Pod Autoscaler

Good luck with your project! 🚀