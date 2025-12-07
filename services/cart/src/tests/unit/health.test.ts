import request from 'supertest';
import app from '../../server';
import mongoose from 'mongoose';

let server = app.listen(3003)

beforeAll(() => {
  // Establish database connection or set up a mock server
  console.log('Database connection established');
});

describe('Healthcheck', () => {
  it('should return 200 OK', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('Running');

  });
});


afterAll(done => {
  // Closing the DB connection allows Jest to exit successfully.
  server.close();
  mongoose.connection.close();
  done()
})