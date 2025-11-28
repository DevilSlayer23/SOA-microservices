import { Router } from "express";
import { Cart } from "../db/schema";
import { Order } from "../db/schema";

const router = Router();



/**
 * GET /cart/:user_id
 * Fetch user cart
 */
router.get("/:user_id", async (req, res): Promise<void> => {
    try {
        const { user_id } = req.params;
        let cart = await Cart.findOne({ user_id, status: "open" });

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

        let cart = await Cart.findOne({ user_id, status: "open" });

        if (!cart) {
            cart = await Cart.create({ user_id, items: [] });
        }

        const existing = cart.items.find(i => i.product_id === product_id);

        if (existing) {
            existing.quantity += quantity;
        } else {
            cart.items.push({ product_id, quantity, price });
        }

        cart.total_items = cart.items.reduce((s : number, i) => s + i.quantity, 0);
        cart.total_price = cart.items.reduce((s : number, i) => s + i.quantity * i.price, 0);

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

        const order = await Order.create({
            user_id,
            items: cart.items,
            total_price: cart.total_price,
            payment_status: "pending",
            order_status: "created"
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

        const cart = await Cart.findOne({ user_id, status: "open" });

        if (!cart) {
            res.json({ message: "Already empty" });
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
