import mongoose from "mongoose";

const orderItemSchema = new mongoose.Schema({
    product_id: { type: Number, required: true },
    quantity: { type: Number, required: true, min: 1 },
    price: { type: Number, required: true },
}, { _id: false });

const orderSchema = new mongoose.Schema({
    order_id : { type: String, required: true, unique: true, index: true },
    user_id: { type: String, required: true, index: true },
    items: {
        type: [orderItemSchema],
        required: true,
        validate: [(items: any[]) => items.length > 0, 'Order must have at least one item']
    },

    total_price: { type: Number, required: true },
    payment_status: {
        type: String,
        enum: ["pending", "paid"],
        default: "pending"
    },
    order_status: {
        type: String,
        enum: ["created", "shipped", "delivered", "cancelled"],
        default: "created"
    },
}, {
    timestamps: true,
    _id: true
});

export const Order = mongoose.model("Order", orderSchema);


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

