import express from 'express';
const mongoose = require('mongoose')
import {db} from "./src/db/db"
import logger from './src/utils/logger';
import e from 'express';

const app = express(); 
const PORT = process.env.PORT || 3000;

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
app.use('/cart', require('./src/cart/route').default);
app.use('/orders', require('./src/orders/route').default);

// Health check endpoint

  app.get('/status', async (req, res) => {
      res.json({
        status: 'Running',
        timestamp: new Date().toISOString()
      });
      
    });


  app.listen(PORT, ( err?: Error) => {
    if (err) {
      logger.error('Failed to start server:' + err.message);
    } else {
      logger.info(`Server is running on port ${PORT}`);
    }
  });
 

export default app;
  