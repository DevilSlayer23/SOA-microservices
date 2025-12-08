import mongoose from "mongoose";
import { Cart } from '../db/schema'; // add .js after compilation


async function removeTotalField() {
    try {
        await mongoose.connect("mongodb://localhost:27017/ecommerce_cart"); // adjust URI if needed
        const result = await Cart.updateMany({}, { $unset: { total: "" } });
        console.log("Removed `total` from documents:", result.modifiedCount);
    } catch (err) {
        console.error("Error:", err);
    } finally {
        await mongoose.disconnect();
    }
}

removeTotalField();
