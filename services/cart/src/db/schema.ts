// ==========================================
// services/cart/src/models/Cart.js
// MongoDB model for shopping cart
// ==========================================

import mongoose from "mongoose";

const cartItemSchema = new mongoose.Schema({
  product_id: {
    type: String,
    required: true
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  quantity: {
    type: Number,
    required: true,
    min: 1
  }
}, { _id: false });


const cartSchema = new mongoose.Schema({
  user_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  items: [cartItemSchema],
  total_items: {
    type: Number,
    default: 0,
  },
  total_price: {
    type: Number,
    default: 0,
  },
  status: {
    type: String,
    enum: ['active', 'inactive', 'pending', "checked_out"], // Allowed statuses
    required: true,
    default: 'pending'
  }
}, {
  timestamps: true,
  collection: 'carts'
});


// Virtual for item count
cartSchema.virtual('itemCount').get(function () {
  return this.items.length;
});

// Ensure virtuals are included in JSON
cartSchema.set('toJSON', { virtuals: true });
cartSchema.set('toObject', { virtuals: true });

export const Cart = mongoose.model('Cart', cartSchema);

