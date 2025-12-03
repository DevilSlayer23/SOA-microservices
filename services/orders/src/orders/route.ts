import express from 'express';
import { Order } from '../db/schema';
import logger from '../utils/logger';
import fastapiClient from '../client/fastapi_user_client';

const router = express.Router();

/**
 * GET /orders
 * Get all orders
 */
router.get('/', async (req, res): Promise<void> => {
  try {
    const orders = await Order.find({});
    if(!orders){
      res.json({"Error" : "Orders not found"});

    } else{
      res.json(orders);
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    res.status(500).json({ error: message });
  }
});

/**
 * GET /orders/user/:userId
 * Get all orders for a specific user ID
 */
router.get('/user/:userId', async (req, res): Promise<void> => {
  try {
    const { userId } = req.params;
    // Use Mongoose's find method to search by the user_id field
    const orders = await Order.find({ user_id: userId });

    if (!orders || orders.length === 0) {
      // It's generally better to return an empty array (200 OK)
      // for a valid search with no results, but 404 is also acceptable
      // if you interpret 'not found' as 'no resources matching criteria'.
      // Sticking to 200 OK with an empty array is common for list endpoints.
      res.status(200).json([]);
      return;
    }

    res.json(orders);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    logger.error(`Error fetching orders by user ID: ${message}`);
    res.status(500).json({ error: message });
  }
});

/**
 * GET /orders/:id
 * Get a specific order by ID
 */
router.get('/:id', async (req, res): Promise<void> => {
  try {
    const { id } = req.params;
    const order = await Order.findById(id);

    if (!order) {
      res.status(404).json({ error: 'Order not found' });
      return;
    }

    res.json(order);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    res.status(500).json({ error: message });
  }
});

/**
 * POST /orders
 * Create a new order
 */
router.post('/', async (req, res): Promise<void> => {
  try {
    logger.info('Creating a new order');
    console.log(req.body);
    const { order_id, user_id, total_price, payment_status, order_status } = req.body;
    const items : any = await fastapiClient.getProduct(req.body.items.product_id);
    const newOrder = await Order.create({
      order_id,
      user_id,
      items,
      total_price,
      payment_status: payment_status || 'pending',
      order_status: order_status || 'created'
    });

    res.status(201).json(newOrder);
    logger.info(`New order created with ID: ${newOrder._id}`);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    logger.error(`Error creating order: ${message}`);
    res.status(500).json({ error: message });
  }
});

/**
 * PUT /orders/:id
 * Update an existing order
 */
router.put('/:id', async (req, res): Promise<void> => {
  try {
    const { id } = req.params;
    const { items, total_price, payment_status, order_status } = req.body;

    const order = await Order.findByIdAndUpdate(
      id,
      {
        ...(items && { items }),
        ...(total_price && { total_price }),
        ...(payment_status && { payment_status }),
        ...(order_status && { order_status })
      },
      { new: true, runValidators: true }
    );

    if (!order) {
      res.status(404).json({ error: 'Order not found' });
      return;
    }

    res.json(order);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    res.status(500).json({ error: message });
  }
});

/**
 * DELETE /orders/:id
 * Delete an order
 */
router.delete('/:id', async (req, res): Promise<void> => {
  try {
    const { id } = req.params;
    const deletedOrder = await Order.findByIdAndDelete(id);

    if (!deletedOrder) {
      res.status(404).json({ error: 'Order not found' });
      return;
    }

    res.status(204).send();
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Unknown error";
    res.status(500).json({ error: message });
  }
});

export default router;
