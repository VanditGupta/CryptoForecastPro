// src/api/test_env.js
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env file
dotenv.config();

// console.log("Testing ACCESS_TOKEN:", process.env.ACCESS_TOKEN);
console.log("Testing API_KEY:", process.env.API_KEY);