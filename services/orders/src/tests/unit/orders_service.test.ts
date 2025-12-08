import request from 'supertest';
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';
import app from '../../server';

let mongoServer: MongoMemoryServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const mongoUri = mongoServer.getUri();
  await mongoose.connect(mongoUri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

afterEach(async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});

describe('Orders Service - Health Check', () => {
  test('GET /health should return OK', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('OK');
  });
});

describe('Orders Service - Add to Orders', () => {
  test('POST /api/orders should add item to orders', async () => {
    const ordersItem = {
      userId: 'test-user-123',
      productId: 'test-product-456',
      quantity: 2
    };

    const response = await request(app)
      .post('/api/orders')
      .send(ordersItem);

    expect(response.status).toBe(201);
    expect(response.body.orders).toBeDefined();
    expect(response.body.orders.items).toHaveLength(1);
  });

  test('POST /api/orders should fail with missing fields', async () => {
    const invalidItem = {
      userId: 'test-user-123'
      // Missing productId and quantity
    };

    const response = await request(app)
      .post('/api/orders')
      .send(invalidItem);

    expect(response.status).toBe(400);
  });
});

describe('Orders Service - Get Orders', () => {
  test('GET /api/orders/:userId should return user orders', async () => {
    const userId = 'test-user-123';

    const response = await request(app).get(`/api/orders/${userId}`);

    expect(response.status).toBe(200);
    expect(response.body.userId).toBe(userId);
  });
});