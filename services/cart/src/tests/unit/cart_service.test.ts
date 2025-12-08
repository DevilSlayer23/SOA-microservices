import request from 'supertest';
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';
import app from '../../server';

let mongoServer: MongoMemoryServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  // const mongoUri = mongoServer.getUri();
  // await mongoose.connect(mongoUri);
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

describe('Cart Service - Health Check', () => {
  test('GET /health should return OK', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('OK');
  });
});

// describe('Cart Service - Add to Cart', () => {
//   test('POST /api/Cart should add item to Cart', async () => {
//     const CartItem = {
//       userId: 'test-user-123',
//       productId: 'test-product-456',
//       quantity: 2
//     };

//     const response = await request(app)
//       .post('/api/Cart')
//       .send(CartItem);

//     expect(response.status).toBe(201);
//     expect(response.body.Cart).toBeDefined();
//     expect(response.body.Cart.items).toHaveLength(1);
//   });

//   test('POST /api/Cart should fail with missing fields', async () => {
//     const invalidItem = {
//       userId: 'test-user-123'
//       // Missing productId and quantity
//     };

//     const response = await request(app)
//       .post('/api/Cart')
//       .send(invalidItem);

//     expect(response.status).toBe(400);
//   });
// });

describe('Cart Service - Get Cart', () => {
  test('GET /api/cart/:userId should return user Cart', async () => {
    const userId = '1';

    const response = await request(app).get(`/api/cart/${userId}`);

    expect(response.status).toBe(200);
    expect(response.body.user_id).toBe(userId);
  });
});