# 🍕 Pizza Mania – Django Web App

A full-stack pizza ordering web application built using Django.
Users can browse pizzas, add items to cart, place orders, and simulate payments.

---

## 🚀 Features

* 🔐 User Authentication (Login / Register / Logout)
* 🍕 Veg & Non-Veg Pizza Categories
* 🛒 Add to Cart System
* 📦 Order Placement & Order History
* 💳 Razorpay Payment Integration *(Demo Mode Supported)*
* 🧾 Invoice Generation
* 📱 Responsive UI using Bootstrap

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite (Development)
* **Payment Gateway:** Razorpay
* **Media Handling:** Local Storage

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/your-username/pizza-mania.git
cd pizza-mania

### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Setup environment variables

Create a `.env` file in the root directory and add:

RAZORPAY_KEY_ID=your_key_here
RAZORPAY_KEY_SECRET=your_secret_here

### 5. Run migrations

python manage.py migrate

### 6. Run the development server

python manage.py runserver

---

## 💳 Payment Note

* Razorpay integration is included
* If API keys are not provided, the app runs in **demo mode**
* No real payment is required for testing

---

## 🔒 Security

* Sensitive data (API keys) is stored using environment variables
* `.env` file is excluded from GitHub using `.gitignore`

---

## 📌 Future Improvements

* 🌐 Deploy project online (Render / AWS)
* 📧 Email notifications for orders
* 🔍 Advanced search & filters
* 📊 Admin dashboard with analytics

---



## ⭐ Note

This project follows best practices like:

* Environment variable management
* Modular Django architecture
* Clean and maintainable code structure

