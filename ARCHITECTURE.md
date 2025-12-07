# System Architecture Documentation

## Overview

This document describes the architecture of the E-Commerce Microservices Platform, including service design, communication patterns, and deployment strategy.

## Table of Contents

1. [Architecture Patterns](#architecture-patterns)
2. [Service Architecture](#service-architecture)
3. [Data Architecture](#data-architecture)
4. [Communication Patterns](#communication-patterns)
5. [Sequence Diagrams](#sequence-diagrams)
6. [Deployment Architecture](#deployment-architecture)
7. [Security Architecture](#security-architecture)

---

## Architecture Patterns

### Microservices Architecture

Our application follows these microservices principles:

- **Single Responsibility**: Each service handles one business domain
- **Autonomous**: Services can be deployed independently
- **Decentralized Data**: Each service owns its database
- **Lightweight Communication**: RESTful HTTP/JSON APIs
- **Infrastructure Automation**: Docker containerization

### Key Design Principles

1. **Service Independence**: Services don't share code or databases
2. **Polyglot Persistence**: Use the best database for each service
3. **Fail Fast**: Services validate inputs and dependencies early
4. **Graceful Degradation**: Services handle downstream failures
5. **Observable**: All services expose health checks and logs

---

## Service Architecture

### High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                         Client Layer                              │
│                   (Web/Mobile Applications)                       │
└────────────┬──────────────┬──────────────┬────────────────────────┘
             │              │              │
             │              │              │
┌────────────▼──────────────▼──────────────▼────────────────────────┐
│                     API Gateway (Future)                          │
│              Load Balancing, Rate Limiting, Auth                  │
└────────┬──────────────┬──────────────┬──────────────┬─────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
   ┌─────────┐    ┌──────────┐   ┌────────┐    ┌──────────┐
   │ Users   │    │ Products │   │  Cart  │    │  Orders  │
   │ Service │    │ Service  │   │ Service│    │ Service  │
   │  :8001  │    │  :8002   │   │  :8003 │    │  :8004   │
   └────┬────┘    └─────┬────┘   └────┬───┘    └─────┬────┘
        │               │             │              │
        │               │             │              │
        ▼               ▼             ▼              ▼
   ┌──────────────────────┐     ┌─────────────────────────┐
   │    PostgreSQL        │     │       MongoDB           │
   │  - ecommerce_users   │     │  - ecommerce_cart       │
   │  - ecommerce_products│     │  - ecommerce_orders     │
   └──────────────────────┘     └─────────────────────────┘
```

### Service Responsibilities

#### 1. Users Service
**Purpose**: Manage user accounts and authentication

**Responsibilities**:
- User registration with email validation
- Password hashing and authentication
- JWT token generation and validation
- User profile management (CRUD)
- Session management

**Technology**: FastAPI (Python), PostgreSQL, SQLAlchemy

**Database Schema**:
```
users
├── id (UUID, Primary Key)
├── email (VARCHAR, UNIQUE, NOT NULL)
├── password_hash (VARCHAR, NOT NULL)
├── name (VARCHAR)
├── phone (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

#### 2. Products Service
**Purpose**: Manage product catalog and inventory

**Responsibilities**:
- Product CRUD operations
- Inventory management (stock tracking)
- Product search and filtering
- Category management
- Price management

**Technology**: FastAPI (Python), PostgreSQL, SQLAlchemy

**Database Schema**:
```
products
├── id (UUID, Primary Key)
├── name (VARCHAR, NOT NULL)
├── description (TEXT)
├── price (DECIMAL, NOT NULL)
├── stock (INTEGER, DEFAULT 0)
├── category (VARCHAR)
├── specifications (JSONB)
├── image_url (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

#### 3. Cart Service
**Purpose**: Manage shopping carts

**Responsibilities**:
- Add/remove items from cart
- Update item quantities
- Validate products with Products Service
- Verify users with Users Service
- Calculate cart totals
- Stock availability checks

**Technology**: Node.js/Express, MongoDB, Mongoose

**Database Schema**:
```javascript
{
  _id: ObjectId,
  userId: String (indexed),
  items: [
    {
      productId: String,
      name: String,
      price: Number,
      quantity: Number
    }
  ],
  total: Number,
  createdAt: Date,
  updatedAt: Date
}
```

#### 4. Orders Service
**Purpose**: Process and manage orders

**Responsibilities**:
- Create orders from cart
- Validate users, products, and cart
- Update product inventory
- Order status management
- Order history tracking
- Handle order cancellations

**Technology**: Node.js/Express, MongoDB, Mongoose

**Database Schema**:
```javascript
{
  _id: ObjectId,
  userId: String (indexed),
  items: [
    {
      productId: String,
      name: String,
      price: Number,
      quantity: Number
    }
  ],
  total: Number,
  shippingAddress: {
    street: String,
    city: String,
    province: String,
    postalCode: String,
    country: String
  },
  paymentMethod: String,
  status: String, // pending, confirmed, processing, shipped, delivered, cancelled, failed
  orderDate: Date,
  updatedAt: Date
}
```

---

## Data Architecture

### Database Per Service Pattern

Each microservice has its own database to ensure:
- Data isolation and independence
- Service autonomy
- Technology flexibility
- Independent scaling

### Database Selection Rationale

**PostgreSQL** (Users & Products):
- Strong ACID compliance for financial data
- Complex queries and relationships
- Data integrity requirements
- Structured data with defined schemas

**MongoDB** (Cart & Orders):
- Flexible schema for varying cart contents
- High write throughput for cart updates
- Document structure matches domain model
- Horizontal scalability

### Data Consistency Strategy

**Eventual Consistency**:
- Cart and Orders use eventual consistency
- Stock updates propagate after order confirmation
- Failed operations trigger compensating transactions

**Strong Consistency**:
- User authentication requires strong consistency
- Product pricing requires strong consistency

---

## Communication Patterns

### Synchronous Communication (REST)

All inter-service communication uses REST APIs:

```
Cart Service ──HTTP GET──> Users Service (verify user)
Cart Service ──HTTP GET──> Products Service (verify product)
Orders Service ──HTTP GET──> Cart Service (get cart)
Orders Service ──HTTP PUT──> Products Service (update stock)
```

### Communication Flow Example

**Adding Item to Cart**:
```
1. Client → Cart Service: POST /api/cart
2. Cart Service → Users Service: GET /api/users/{userId}
3. Users Service → Cart Service: User data
4. Cart Service → Products Service: GET /api/products/{productId}
5. Products Service → Cart Service: Product data + stock
6. Cart Service → Database: Save cart
7. Cart Service → Client: Cart with added item
```

### Error Handling

Services implement circuit breaker pattern:
- Timeout after 5 seconds
- Retry failed requests (exponential backoff)
- Return cached data when available
- Graceful degradation

---

## Sequence Diagrams

### 1. User Registration Flow

```
┌──────┐          ┌──────────────┐           ┌──────────┐
│Client│          │Users Service │           │PostgreSQL│
└──┬───┘          └──────┬───────┘           └────┬─────┘
   │                     │                        │
   ├──POST /register────►│                        │
   │  {email, password}  │                        │
   │                     │                        │
   │                     ├──Hash password─────────┤
   │                     │                        │
   │                     ├──INSERT user───────────►
   │                     │                        │
   │                     ◄──User created──────────┤
   │                     │                        │
   │                     ├──Generate JWT──────────┤
   │                     │                        │
   │◄──201 Created───────┤                        │
   │  {user, token}      │                        │
   │                     │                        │
```

### 2. Add to Cart Flow

```
┌──────┐  ┌────────────┐  ┌──────────────┐  ┌────────────────┐  ┌───────┐
│Client│  │Cart Service│  │Users Service │  │Products Service│  │MongoDB│
└──┬───┘  └─────┬──────┘  └──────┬───────┘  └────────┬───────┘  └───┬───┘
   │            │                 │                   │              │
   ├─POST /cart─►                 │                   │              │
   │ {userId,   │                 │                   │              │
   │ productId, │                 │                   │              │
   │ quantity}  │                 │                   │              │
   │            │                 │                   │              │
   │            ├─GET /users/{id}─►                   │              │
   │            │                 │                   │              │
   │            │◄─User exists────┤                   │              │
   │            │                 │                   │              │
   │            ├─GET /products/{id}──────────────────►              │
   │            │                 │                   │              │
   │            │◄─Product + stock────────────────────┤              │
   │            │                 │                   │              │
   │            ├─Check stock > qty                   │              │
   │            │                 │                   │              │
   │            ├─Save cart──────────────────────────────────────────►
   │            │                 │                   │              │
   │            │◄─Saved─────────────────────────────────────────────┤
   │            │                 │                   │              │
   │◄─201 Cart──┤                 │                   │              │
   │            │                 │                   │              │
```

### 3. Create Order Flow

```
┌──────┐  ┌──────────────┐  ┌────────────┐  ┌────────────────┐  ┌──────────────┐  ┌───────┐
│Client│  │Orders Service│  │Cart Service│  │Products Service│  │Users Service │  │MongoDB│
└──┬───┘  └──────┬───────┘  └─────┬──────┘  └────────┬───────┘  └──────┬───────┘  └───┬───┘
   │             │                 │                  │                 │              │
   ├─POST /orders►                 │                  │                 │              │
   │ {userId,    │                 │                  │                 │              │
   │ address}    │                 │                  │                 │              │
   │             │                 │                  │                 │              │
   │             ├─GET /users/{id}─────────────────────────────────────►│              │
   │             │                 │                  │                 │              │
   │             │◄─User exists─────────────────────────────────────────┤              │
   │             │                 │                  │                 │              │
   │             ├─GET /cart/{userId}───►             │                 │              │
   │             │                 │                  │                 │              │
   │             │◄─Cart items─────┤                  │                 │              │
   │             │                 │                  │                 │              │
   │             ├─Verify products────────────────────►                 │              │
   │             │                 │                  │                 │              │
   │             │◄─All available─────────────────────┤                 │              │
   │             │                 │                  │                 │              │
   │             ├─Create order────────────────────────────────────────────────────────►
   │             │                 │                  │                 │              │
   │             │◄─Order saved────────────────────────────────────────────────────────┤
   │             │                 │                  │                 │              │
   │             ├─Update stock (for each item)───────►                 │              │
   │             │                 │                  │                 │              │
   │             │◄─Stock updated─────────────────────┤                 │              │
   │             │                 │                  │                 │              │
   │             ├─DELETE /cart/{userId}─►            │                 │              │
   │             │                 │                  │                 │              │
   │             │◄─Cart cleared───┤                  │                 │              │
   │             │                 │                  │                 │              │
   │◄─201 Order──┤                 │                  │                 │              │
   │             │                 │                  │                 │              │
```

---

## Deployment Architecture

### Docker Containerization

Each service runs in its own container:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                          │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Users Service│  │Products Svc  │  │ Cart Service │   │
│  │ Container    │  │ Container    │  │ Container    │   │
│  │ Python:3.11  │  │ Python:3.11  │  │ Node:20      │   │
│  │ Port: 8001   │  │ Port: 8002   │  │ Port: 8003   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │Orders Service│  │ PostgreSQL   │  │  MongoDB     │   │
│  │ Container    │  │ Container    │  │  Container   │   │
│  │ Node:20      │  │ Postgres:17  │  │  Mongo:8.0   │   │
│  │ Port: 8004   │  │ Port: 5432   │  │  Port: 27017 │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│         ┌──────────────────────────────┐                │
│         │   Backend Network (bridge)   │                │
│         │  All containers connected    │                │
│         └──────────────────────────────┘                │
│                                                         │
│      ┌─────────────┐        ┌──────────────┐            │
│      │  pgdata     │        │  mongodata   │            │
│      │  Volume     │        │  Volume      │            │
│      └─────────────┘        └──────────────┘            │
└─────────────────────────────────────────────────────────┘
```

### Container Health Checks

All containers implement health checks:

- **Databases**: Connection tests every 10 seconds
- **Services**: HTTP health endpoint checks every 10 seconds
- **Start Period**: 30-40 seconds for service initialization
- **Retries**: 5-10 attempts before marking unhealthy

### Service Dependencies

```yaml
Orders Service depends on:
  ├── MongoDB (healthy)
  ├── Users Service (healthy)
  ├── Products Service (healthy)
  └── Cart Service (healthy)

Cart Service depends on:
  ├── MongoDB (healthy)
  ├── Users Service (healthy)
  └── Products Service (healthy)

Users/Products Services depend on:
  └── PostgreSQL (healthy)
```

### Network Isolation

**Backend Network**:
- All services communicate through dedicated Docker network
- Services discover each other via DNS (service names)
- Databases not exposed to host (internal only)
- Only service ports exposed to host

---

## Security Architecture

### Container Security

1. **Non-root Users**: All containers run as non-root users
   ```dockerfile
   RUN useradd --create-home appuser
   USER appuser
   ```

2. **Minimal Base Images**: Using slim/alpine variants
3. **No Secrets in Images**: Environment variables for sensitive data
4. **Read-only Filesystems** (future enhancement)

### Application Security

1. **Authentication**: JWT-based authentication (Users Service)
2. **Password Hashing**: bcrypt with salt rounds
3. **Input Validation**: Request validation on all endpoints
4. **SQL Injection Protection**: Parameterized queries (SQLAlchemy)
5. **CORS**: Configured for specific origins (production)

### Data Security

1. **Encryption at Rest**: Database volumes (future enhancement)
2. **Encryption in Transit**: HTTPS (production)
3. **Database Credentials**: Environment variables, not hardcoded
4. **Sensitive Data**: Never logged or exposed in errors

### Network Security

1. **Internal Network**: Backend network isolated from external
2. **Firewall Rules**: Only necessary ports exposed
3. **Rate Limiting** (future): Prevent abuse
4. **API Gateway** (future): Single entry point with security policies

---

## Scalability Considerations

### Horizontal Scaling

Each service can be scaled independently:

```yaml
docker-compose up --scale ecom_users=3 --scale ecom_products=3
```

### Load Balancing (Future)

Add nginx or traefik for load balancing:
```
Client → Load Balancer → [Service Instance 1, 2, 3...]
```

### Database Scaling

- **PostgreSQL**: Read replicas for read-heavy workloads
- **MongoDB**: Sharding for horizontal scaling

### Caching (Future Enhancement)

Add Redis for:
- Session storage
- Product catalog caching
- Cart data caching

---

## Monitoring and Observability

### Health Checks

All services expose `/health` endpoints:
- Database connectivity
- Service status
- Dependency health

### Logging Strategy

- **Application Logs**: JSON structured logs
- **Container Logs**: Docker log driver
- **Centralized Logging** (future): ELK stack or Fluentd

### Metrics (Future)

- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Key Metrics**: Request rate, error rate, duration

---

## Future Enhancements

1. **API Gateway**: Kong or Nginx for unified entry point
2. **Message Queue**: RabbitMQ/Kafka for async communication
3. **Service Mesh**: Istio for advanced traffic management
4. **Distributed Tracing**: Jaeger or Zipkin
5. **CI/CD Pipeline**: GitHub Actions or Jenkins
6. **Kubernetes Deployment**: Migrate from Docker Compose
7. **Caching Layer**: Redis for performance
8. **Event-Driven Architecture**: For real-time updates