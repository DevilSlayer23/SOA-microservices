// ==========================================
// services/orders/src/models/Order.js
// MongoDB model for orders
// ==========================================

import mongoose from "mongoose";

const orderItemSchema = new mongoose.Schema({
  productId: {
    type: String,
    required: true
  },
  name: {
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

const shippingAddressSchema = new mongoose.Schema({
  street: {
    type: String,
    required: true
  },
  city: {
    type: String,
    required: true
  },
  province: {
    type: String,
    required: false
  },
  postalCode: {
    type: String,
    required: true
  },
  country: {
    type: String,
    required: true,
    default: 'Canada'
  }
}, { _id: false });

const orderSchema = new mongoose.Schema({
  userId: {
    type: String,
    required: true,
    index: true
  },
  items: {
    type: [orderItemSchema],
    validate: {
      validator: function(items: string | any[]) {
        return items && items.length > 0;
      },
      message: 'Order must have at least one item'
    }
  },
  total: {
    type: Number,
    required: true,
    min: 0
  },
  shippingAddress: {
    type: shippingAddressSchema,
    required: true
  },
  paymentMethod: {
    type: String,
    required: true,
    enum: ['credit_card', 'debit_card', 'paypal', 'cash_on_delivery']
  },
  status: {
    type: String,
    required: true,
    enum: ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'failed'],
    default: 'pending',
    index: true
  },
  failureReason: {
    type: String,
    required: false
  },
  orderDate: {
    type: Date,
    default: Date.now,
    index: true
  },
  trackingNumber: {
    type: String,
    required: false
  }
}, {
  timestamps: true,
  collection: 'orders'
});

// Index for querying user's orders
orderSchema.index({ userId: 1, orderDate: -1 });

// Index for querying by status
orderSchema.index({ status: 1, orderDate: -1 });

// Calculate total before saving
orderSchema.pre('save', function(next) {
  if (this.items && this.items.length > 0) {
    this.total = this.items.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
  }
  next();
});

// Virtual for total items
orderSchema.virtual('totalItems').get(function() {
  return this.items.reduce((sum, item) => sum + item.quantity, 0);
});

// Ensure virtuals are included in JSON
orderSchema.set('toJSON', { virtuals: true });
orderSchema.set('toObject', { virtuals: true });

export const Order = mongoose.model('Order', orderSchema);

