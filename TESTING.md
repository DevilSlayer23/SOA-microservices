# Testing Guide

Complete testing guide for the E-Commerce Microservices Platform.

## Table of Contents

1. [Quick Start Testing](#quick-start-testing)
2. [Manual Testing](#manual-testing)
3. [Integration Testing](#integration-testing)
4. [End-to-End Testing](#end-to-end-testing)
5. [Load Testing](#load-testing)
6. [Debugging](#debugging)

---

## Quick Start Testing

### Verify All Services Are Running

```bash
# Check all container status
docker-compose ps

# All services should show "healthy"
# Expected output:
# NAME            STATUS
# users      Up (healthy)
# products   Up (healthy)
# cart       Up (healthy)
# orders     Up (healthy)
# postgres        Up (healthy)
# mongo           Up (healthy)
```

### Test Health Endpoints

```bash
# Test all services
curl http://localhost:8001/health  # Users Service
curl http://localhost:8002/health  # Products Service
curl http://localhost:8003/health  # Cart Service
curl http://localhost:8004/health  # Orders Service

# Expected: {"status":"OK",...}
```

---

## Manual Testing

### 1. Users Service Tests

#### Register a New User

```bash
curl -X POST http://localhost:8001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!",
    "name": "John Doe",
    "phone": "+1234567890"
  }'
```

**Expected Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "created_at": "2024-12-02T10:30:00Z"
}
```

**Save the `id` for later tests!**

#### Login User

```bash
curl -X POST http://localhost:8001/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "name": "John Doe"
  }
}
```

**Save the `access_token` for authenticated requests!**

#### Get User Profile

```bash
USER_ID="550e8400-e29b-41d4-a716-446655440000"
TOKEN="your-token-here"

curl http://localhost:8001/api/users/$USER_ID \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Products Service Tests

#### Create Products

```bash
# Create Product 1 - Laptop
curl -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro",
    "description": "16-inch, M3 Pro chip, 18GB RAM",
    "price": 2499.99,
    "stock": 50,
    "category": "Electronics"
  }'

# Create Product 2 - Mouse
curl -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse with USB receiver",
    "price": 29.99,
    "stock": 200,
    "category": "Accessories"
  }'

# Create Product 3 - Keyboard
curl -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mechanical Keyboard",
    "description": "RGB backlit mechanical keyboard",
    "price": 149.99,
    "stock": 75,
    "category": "Accessories"
  }'
```

**Save the product IDs from responses!**

#### Get All Products

```bash
curl http://localhost:8002/api/products
```

#### Get Product by ID

```bash
PRODUCT_ID="your-product-id"
curl http://localhost:8002/api/products/$PRODUCT_ID
```

#### Search Products

```bash
# Search by category
curl "http://localhost:8002/api/products?category=Electronics"

# Search with price range
curl "http://localhost:8002/api/products?min_price=100&max_price=500"

# Search by keyword
curl "http://localhost:8002/api/products?search=wireless"
```

### 3. Cart Service Tests

#### Add Item to Cart

```bash
USER_ID="550e8400-e29b-41d4-a716-446655440000"
PRODUCT_ID="your-laptop-product-id"

curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$PRODUCT_ID'",
    "quantity": 1
  }'
```

**Expected Response** (201 Created):
```json
{
  "message": "Item added to cart",
  "cart": {
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "productId": "prod-123",
        "name": "MacBook Pro",
        "price": 2499.99,
        "quantity": 1
      }
    ],
    "total": 2499.99
  }
}
```

#### Add More Items

```bash
# Add mouse to cart
MOUSE_ID="your-mouse-product-id"

curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$MOUSE_ID'",
    "quantity": 2
  }'

# Add keyboard to cart
KEYBOARD_ID="your-keyboard-product-id"

curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$KEYBOARD_ID'",
    "quantity": 1
  }'
```

#### Get Cart

```bash
curl http://localhost:8003/api/cart/$USER_ID
```

**Expected Response**:
```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "productId": "prod-123",
      "name": "MacBook Pro",
      "price": 2499.99,
      "quantity": 1
    },
    {
      "productId": "prod-456",
      "name": "Wireless Mouse",
      "price": 29.99,
      "quantity": 2
    },
    {
      "productId": "prod-789",
      "name": "Mechanical Keyboard",
      "price": 149.99,
      "quantity": 1
    }
  ],
  "total": 2709.96,
  "itemCount": 3
}
```

#### Update Cart Item Quantity

```bash
curl -X PUT http://localhost:8003/api/cart/$USER_ID/items/$MOUSE_ID \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3
  }'
```

#### Remove Item from Cart

```bash
curl -X DELETE http://localhost:8003/api/cart/$USER_ID/items/$KEYBOARD_ID
```

### 4. Orders Service Tests

#### Create Order from Cart

```bash
curl -X POST http://localhost:8004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "shippingAddress": {
      "street": "123 Main Street",
      "city": "Toronto",
      "province": "Ontario",
      "postalCode": "M5H 2N2",
      "country": "Canada"
    },
    "paymentMethod": "credit_card"
  }'
```

**Expected Response** (201 Created):
```json
{
  "message": "Order created successfully",
  "order": {
    "id": "order-abc123",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "productId": "prod-123",
        "name": "MacBook Pro",
        "price": 2499.99,
        "quantity": 1
      },
      {
        "productId": "prod-456",
        "name": "Wireless Mouse",
        "price": 29.99,
        "quantity": 3
      }
    ],
    "total": 2589.96,
    "status": "confirmed",
    "orderDate": "2024-12-02T14:30:00Z"
  }
}
```

**Save the order `id`!**

#### Verify Cart Was Cleared

```bash
curl http://localhost:8003/api/cart/$USER_ID

# Expected: Empty cart with total 0
```

#### Verify Product Stock Was Updated

```bash
curl http://localhost:8002/api/products/$PRODUCT_ID

# Stock should be decreased by ordered quantity
```

#### Get User's Orders

```bash
curl http://localhost:8004/api/orders/user/$USER_ID
```

#### Get Specific Order

```bash
ORDER_ID="order-abc123"
curl http://localhost:8004/api/orders/$ORDER_ID
```

#### Update Order Status

```bash
curl -X PUT http://localhost:8004/api/orders/$ORDER_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'

# Then update to shipped
curl -X PUT http://localhost:8004/api/orders/$ORDER_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped"
  }'

# Finally to delivered
curl -X PUT http://localhost:8004/api/orders/$ORDER_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "delivered"
  }'
```

---

## Integration Testing

### Complete E-Commerce Flow Test Script

Save this as `test_complete_flow.sh`:

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== E-Commerce Microservices Integration Test ===${NC}\n"

# Step 1: Register User
echo -e "${GREEN}Step 1: Registering new user...${NC}"
USER_RESPONSE=$(curl -s -X POST http://localhost:8001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test'$(date +%s)'@example.com",
    "password": "TestPass123!",
    "name": "Test User"
  }')

USER_ID=$(echo $USER_RESPONSE | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
echo "User ID: $USER_ID"

# Step 2: Create Products
echo -e "\n${GREEN}Step 2: Creating products...${NC}"
PRODUCT1=$(curl -s -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Laptop",
    "description": "Test laptop for integration",
    "price": 999.99,
    "stock": 100,
    "category": "Electronics"
  }')

PRODUCT1_ID=$(echo $PRODUCT1 | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
echo "Product 1 ID: $PRODUCT1_ID"

PRODUCT2=$(curl -s -X POST http://localhost:8002/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Mouse",
    "description": "Test mouse for integration",
    "price": 29.99,
    "stock": 200,
    "category": "Accessories"
  }')

PRODUCT2_ID=$(echo $PRODUCT2 | grep -o '"id":"[^"]*' | grep -o '[^"]*$')
echo "Product 2 ID: $PRODUCT2_ID"

# Step 3: Add items to cart
echo -e "\n${GREEN}Step 3: Adding items to cart...${NC}"
curl -s -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$PRODUCT1_ID'",
    "quantity": 1
  }' | jq '.'

curl -s -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$PRODUCT2_ID'",
    "quantity": 2
  }' | jq '.'

# Step 4: View cart
echo -e "\n${GREEN}Step 4: Viewing cart...${NC}"
curl -s http://localhost:8003/api/cart/$USER_ID | jq '.'

# Step 5: Create order
echo -e "\n${GREEN}Step 5: Creating order from cart...${NC}"
ORDER_RESPONSE=$(curl -s -X POST http://localhost:8004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "shippingAddress": {
      "street": "123 Test St",
      "city": "Toronto",
      "postalCode": "M1M 1M1",
      "country": "Canada"
    },
    "paymentMethod": "credit_card"
  }')

echo $ORDER_RESPONSE | jq '.'
ORDER_ID=$(echo $ORDER_RESPONSE | grep -o '"id":"[^"]*' | grep -o '[^"]*$')

# Step 6: Verify cart is cleared
echo -e "\n${GREEN}Step 6: Verifying cart is cleared...${NC}"
curl -s http://localhost:8003/api/cart/$USER_ID | jq '.'

# Step 7: Verify stock was updated
echo -e "\n${GREEN}Step 7: Verifying stock was updated...${NC}"
curl -s http://localhost:8002/api/products/$PRODUCT1_ID | jq '.stock'
curl -s http://localhost:8002/api/products/$PRODUCT2_ID | jq '.stock'

# Step 8: View order
echo -e "\n${GREEN}Step 8: Viewing created order...${NC}"
curl -s http://localhost:8004/api/orders/$ORDER_ID | jq '.'

echo -e "\n${BLUE}=== Test Complete ===${NC}"
```

Make it executable and run:

```bash
chmod +x test_complete_flow.sh
./test_complete_flow.sh
```

---

## End-to-End Testing

### Testing Error Scenarios

#### 1. Test Invalid User

```bash
# Try to add to cart with non-existent user
curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "non-existent-user-id",
    "productId": "some-product-id",
    "quantity": 1
  }'

# Expected: 404 Not Found - User not found
```

#### 2. Test Invalid Product

```bash
# Try to add non-existent product to cart
curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "non-existent-product",
    "quantity": 1
  }'

# Expected: 404 Not Found - Product not found
```

#### 3. Test Insufficient Stock

```bash
# Try to add more items than available
curl -X POST http://localhost:8003/api/cart \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "productId": "'$PRODUCT_ID'",
    "quantity": 999999
  }'

# Expected: 400 Bad Request - Insufficient stock
```

#### 4. Test Empty Cart Order

```bash
# Try to create order with empty cart
curl -X POST http://localhost:8004/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'$USER_ID'",
    "shippingAddress": {...},
    "paymentMethod": "credit_card"
  }'

# Expected: 400 Bad Request - Cart is empty
```

#### 5. Test Order Cancellation

```bash
# Cancel an order
curl -X DELETE http://localhost:8004/api/orders/$ORDER_ID

# Expected: Order status changed to cancelled
# Stock should be restored
```

---

## Load Testing

### Using Apache Bench

```bash
# Test Users Service health endpoint
ab -n 1000 -c 10 http://localhost:8001/health

# Test Products Service - Get all products
ab -n 500 -c 5 http://localhost:8002/api/products
```

### Using wrk (more advanced)

```bash
# Install wrk
sudo apt install wrk  # Ubuntu/Debian

# Test health endpoints
wrk -t4 -c100 -d30s http://localhost:8001/health

# Test with POST request
wrk -t4 -c100 -d30s -s post.lua http://localhost:8003/api/cart
```

---

## Debugging

### View Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f users
docker-compose logs -f products
docker-compose logs -f cart
docker-compose logs -f orders

# View database logs
docker-compose logs -f postgres
docker-compose logs -f mongo

# View last 100 lines
docker-compose logs --tail=100 users
```

### Check Database Contents

#### PostgreSQL

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U admin -d ecommerce_users

# List all users
SELECT * FROM users;

# Connect to products database
docker-compose exec postgres psql -U admin -d ecommerce_products

# List all products
SELECT * FROM products;

# Exit
\q
```

#### MongoDB

```bash
# Connect to MongoDB
docker-compose exec mongo mongosh

# Switch to cart database
use ecommerce_cart

# List all carts
db.carts.find().pretty()

# Switch to orders database
use ecommerce_orders

# List all orders
db.orders.find().pretty()

# Exit
exit
```

### Check Container Health

```bash
# Check container status
docker-compose ps

# Inspect container health
docker inspect <container_name> | grep -A 10 Health

# Check resource usage
docker stats
```

### Restart Services

```bash
# Restart specific service
docker-compose restart users

# Rebuild and restart
docker-compose up -d --build users

# Restart all services
docker-compose restart
```

---

## Test Checklist

Before submitting your project, verify:

- [ ] All services start successfully
- [ ] All health checks pass
- [ ] User registration and login work
- [ ] Product CRUD operations work
- [ ] Cart operations work (add, update, remove)
- [ ] Order creation works
- [ ] Inter-service communication works
- [ ] Stock updates after order
- [ ] Cart clears after order
- [ ] Error handling works (invalid user, product, stock)
- [ ] Database persistence works (restart containers)
- [ ] All API endpoints documented
- [ ] Architecture diagrams created
- [ ] README with setup instructions

---

## Performance Benchmarks

Expected performance on local machine:

- **Health Checks**: < 50ms
- **User Registration**: < 200ms
- **Product Search**: < 100ms
- **Add to Cart**: < 300ms (includes 2 external calls)
- **Create Order**: < 500ms (includes multiple external calls and DB updates)

If responses are slower, check:
- Database connection pool settings
- Network latency between containers
- Container resource allocation
- Service health status