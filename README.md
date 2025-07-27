ProxiMart — Inventory & Order Management for Street Food Vendors

📌 Project Overview
ProxiMart is a full-stack web application aimed at digitizing inventory and order management for Indian street food vendors. The system helps vendors efficiently track raw materials, monitor stock levels, receive low-stock alerts, and view recent orders — ultimately streamlining sourcing and reducing wastage.

💡 What the Project Does
🔐 Inventory Management
Tracks raw materials and ingredients with:

Name

Quantity

Price

Unit (e.g., kg, litre)

Category (e.g., Veggies, Spices)

Threshold (for low-stock alerts)

Provides real-time updates to help vendors stay informed on stock levels.

📦 Order Management
Displays recent orders with:

Ordered items and their quantities

Total prices

Timestamps of order placement

⚙ Backend
Built using Flask and Firebase Firestore

Vendor-specific storage and retrieval of inventory and orders

RESTful API routes for:

Add, update, delete, and retrieve inventory items

Fetch recent orders

Filter data by vendor ID

💻 Frontend
Developed with React and Tailwind CSS

Dynamically fetches inventory and order data for vendors (vendor1 by default)

Includes components like:

Inventory.jsx

InventoryItem.jsx

Handles:

Asynchronous API requests using React Hooks

Conditional rendering for error or empty data cases

✅ How It Solves the Problem
The original problem focused on helping street food vendors source raw materials efficiently.

Our Solution:
📊 Real-time inventory visibility enables better planning and stock control.

📈 Order history helps manage demand and optimize restocking.

🔐 Vendor-specific data ensures secure, personalized experience.

🧑‍💻 User-friendly UI tailored to vendor workflow.

📲 Extendable API paves the way for future integration with local suppliers and analytics.

🚀 Features Implemented
 Vendor-based inventory CRUD via Flask API

 Low-stock alert system based on thresholds

 Fetch and render real-time inventory/order data

 React UI components for structured display

 Firestore-backed data structure for easy scaling

 Error handling and fallback UI for empty data

🛠 Technologies Used
Category	Tech Stack
Frontend	React, Tailwind CSS
Backend	Flask (Python)
Database	Firebase Firestore
API Format	REST with JSON responses

⚙ Setup Instructions
📁 Backend (Flask)
Create a Firebase project and configure Firestore.

Set up Firebase credentials (JSON) and integrate with Flask.

Start backend server:

bash
Copy
Edit
flask run
Runs at: http://localhost:5000/api

🌐 Frontend (React)
Navigate to the frontend directory.

Install dependencies:

bash
Copy
Edit
npm install
Start development server:

bash
Copy
Edit
npm start
App runs at: http://localhost:3000

🧪 Usage
App loads inventory and orders for vendor1 by default.

Vendors can:

View current stock levels and item details.

Get alerts for low-stock items.

See recent order history with timestamped details.

🔮 Future Improvements
🔐 Add login and multi-vendor authentication

🛍 Enable placing supply orders directly through app

🔔 Real-time notifications for low stock or new orders

📊 Analytics dashboard for sales and usage trends

📌 Project Status
This project successfully demonstrates the core features of inventory and order tracking, providing a strong foundation to help street food vendors manage raw materials more efficiently.

👨‍👩‍👧‍👦 Team Members
Mayank Sangwan

Mansi Bisht

Divya Pant

Aayushi Chhindra
