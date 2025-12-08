// Generate database connection and export it 
import mongoose from "mongoose";

// mongoose.connect(mongoURI)
//     .then(() => {
//     })
//     .catch((err) => {
//         console.error("Error connecting to MongoDB:", err);
//     });

// export const db = mongoose.connection;

const MONGO_URI = process.env.MONGO_DB_URI || 'mongodb://localhost:27017/ecommerce_cart';

export const db = async () => {
    console.log("Mongo URI: " + MONGO_URI)
    try {
        await mongoose.connect(MONGO_URI);

        console.log('✅ MongoDB connected successfully (Cart Service)');
        console.log(`📦 Database: ${mongoose.connection.name}`);

        mongoose.connection.on('error', (err) => {
            console.error('❌ MongoDB connection error:', err);
        });

        mongoose.connection.on('disconnected', () => {
            console.warn('⚠️  MongoDB disconnected');
        });

        mongoose.connection.on('reconnected', () => {
            console.log('✅ MongoDB reconnected');
        });

    } catch (error) {
        console.error('❌ MongoDB connection failed:', error || "");
        process.exit(1);
    }
};



