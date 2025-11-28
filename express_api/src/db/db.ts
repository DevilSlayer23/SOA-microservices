// Generate database connection and export it 
import mongoose from "mongoose";

const mongoURI = process.env.MONGO_URI || "mongodb://localhost:27017/express_api";

mongoose.connect(mongoURI)
    .then(() => {
    })
    .catch((err) => {
        console.error("Error connecting to MongoDB:", err);
    });

export const db = mongoose.connection;

