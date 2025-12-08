import { Router } from "express";
import { Cart } from "../db/schema";
import createApiClient from "../services/ApiService";
import { config } from "dotenv";


const router = Router();

const api = createApiClient(
    {
        baseURL: 'http://localhost:8003/',
        retries: 2

    });

/**
* GET /cart/:
* Fetch user cart
*/

/**
 * GET /cart/:user_id
 * Fetch user cart
 */
router.get("/:user_id", async (req, res): Promise<void> => {
    try {
        const { user_id } = req.params;
        let cart = await Cart.findOne({ user_id });

        if (!cart) {
            cart = await Cart.create({ user_id, items: [] });
        }

        res.json(cart);
    } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Unknown error";
        res.status(500).json({ error: message });
    }
});

/**
 * POST /cart/:user_id/add
 * Add an item to cart
 */
router.post("/:user_id/add", async (req, res): Promise<void> => {
    try {
        const { user_id } = req.params;
        const { product_id, quantity, price } = req.body;

        console.log(req.body);

        let cart = await Cart.findOne({ user_id });

        if (!cart) {
            cart = await Cart.create({ user_id, items: [] });
        }

        const existing = cart.items.find(item => item.product_id === product_id);

        if (existing) {
            existing.quantity += quantity;
        } else {
            cart.items.push({ product_id, quantity, price });
        }

        cart.total_items = cart.items.reduce((s: number, item) => s + item.quantity, 0);
        cart.total_price = cart.items.reduce((s: number, item) => s + item.quantity * item.price, 0);

        await cart.save();

        res.json(cart);

    } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Unknown error";
        res.status(500).json({ error: message });
    }
});

/**
 * POST /cart/:user_id/checkout
 * Convert cart → order
 */
router.post("/:user_id/checkout", async (req, res): Promise<void> => {
    try {
        const { user_id } = req.params;

        const cart = await Cart.findOne({ user_id, status: "open" });

        if (!cart || cart.items.length === 0) {
            res.status(400).json({ error: "Cart empty" });
            return;
        }

        const order = api.get("/api/orders", {
        });

        cart.status = "checked_out";
        await cart.save();

        res.json(order);

    } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Unknown error";
        res.status(500).json({ error: message });
    }
});

/**
 * DELETE /cart/:user_id/clear
 */
router.delete("/:user_id/clear", async (req, res): Promise<void> => {
    try {
        const { user_id } = req.params;

        const cart = await Cart.findOne({ user_id });

        if (!cart) {
            res.json({ message: "Cart already empty" });
            return;
        }

        cart.items.splice(0);  // Clears the array
        cart.total_items = 0;
        cart.total_price = 0;

        await cart.save();

        res.json({ message: "Cleared" });

    } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Unknown error";
        res.status(500).json({ error: message });
    }
});

export default router;
