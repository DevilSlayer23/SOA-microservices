const env = process.env.NODE_ENV;

if (env === 'production') {
  require('dotenv').config({ path: '.env.prod' });
} else {
  require('dotenv').config({ path: '.env.local' });
}

console.log("Loaded env file:", env === 'production' ? ".env.prod" : ".env.local");

import express from 'express';
import cors from 'cors';
import {db} from "./src/db/db"


const app = express(); 
const PORT = process.env.APP_PORT || 8004;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



// Start server
const startServer = async () => {
  try {
    // Connect to MongoDB
    await db();

    // Start Express server
    app.listen(Number(PORT), '0.0.0.0', () => {
      console.log(`🚀 Cart Service running on port ${PORT}`);
      console.log(`📍 Health check: http://localhost:${PORT}/health`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
};

startServer();

// Import and use cart and orders routes
app.use('/api/orders', require('./src/orders/route').default);

// Health check endpoint

app.get('/health', async (req, res) => {
    res.json({
      status: 'Running',
      timestamp: new Date().toISOString()
    });
    
  });

 
  // Root endpoint
app.get('/', (req, res) => {
  res.json({ 
    message: 'Cart Service API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      cart: '/api/cart'
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});





export default app;
  