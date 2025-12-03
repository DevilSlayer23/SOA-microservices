import mongoose from "mongoose";

const cartItemSchema = new mongoose.Schema({
    product_id: { type: Number, required: true },
    quantity: { type: Number, required: true, min: 1 },
    price: { type: Number, required: true },
}, { _id: false });

const cartSchema = new mongoose.Schema({
    user_id: { type: String, required: true, index: true },
    items: {
        type: [cartItemSchema],
        default: []
    },
    status: {
        type: String,
        enum: ["open", "checked_out"],
        default: "open",
    },
    total_price: { type: Number, default: 0 },
    total_items: { type: Number, default: 0 },
}, {
    timestamps: true
});

export const Cart = mongoose.model("Cart", cartSchema);

