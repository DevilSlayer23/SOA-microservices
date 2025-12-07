const env = process.env.NODE_ENV;

if (env === 'production') {
  require('dotenv').config({ path: '.env.prod' });
} else {
  require('dotenv').config({ path: '.env.local' });
}

console.log("Loaded env file:", env === 'production' ? ".env.prod" : ".env.local");

import express from 'express';
const mongoose = require('mongoose')
import { db } from "./db/db"
import logger from './utils/logger';

const app = express();
const PORT = process.env.APP_PORT || 8003;

db.on('error', (err: unknown) => {
  const message = err instanceof Error ? err.message : String(err);
  // Use a single string (or structured object if your logger's types accept it)
  logger.error(`Failed to start server: ${message}`);
});

db.once("open", () => {
  logger.info("Connected to MongoDB database");
});


// Middleware to parse JSON bodies
app.use(express.json());

// Import and use cart and orders routes
app.use('/api/cart', require('./cart/route').default);


// Health check endpoint

app.get('/health', async (req, res) => {
  res.json({
    status: 'Running',
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