const env = process.env.NODE_ENV;

if (env === 'production') {
  require('dotenv').config({ path: '.env.prod' });
} else {
  require('dotenv').config({ path: '.env.local' });
}

console.log("Loaded env file:", env === 'production' ? ".env.prod" : ".env.local");

import express from 'express';
import cors from 'cors';
import { db } from "./db/db"
import logger from './utils/logger';


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
app.use('/api/cart', require('./cart/route').default);


// Health check endpoint

app.get('/health', async (req, res) => {
  res.json({
    status: 'OK',
    app: 'Cart',
    timestamp: new Date().toISOString()
  });

});


app.listen(PORT, (err?: Error) => {
  if (err) {
    logger.error('Failed to start server:' + err.message);
  } else {
    logger.info(`Server is running on port ${PORT}`);
  }
});


export default app;
// This is test