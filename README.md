# 🍔 Foodie - Restaurant Ordering Platform

Foodie is a full-stack restaurant ordering platform inspired by Zomato. It allows customers to browse restaurants, view menus, manage carts, place orders, track order history, save favorite restaurants, and receive personalized recommendations. Restaurant owners can manage their restaurants, menus, and orders through a dedicated dashboard.

---

# Features

## Customer

- User Registration & Login (JWT Authentication)
- Browse Restaurants
- Search Restaurants
- Filter Restaurants
- View Restaurant Details
- View Restaurant Menu
- Add Items to Cart
- Update Cart Quantity
- Remove Items from Cart
- Place Orders
- View Order History
- Manage Profile
- Save Favorite Restaurants
- Manage Food Preferences
- Personalized Restaurant Recommendations

## Restaurant Owner

- Owner Registration & Login
- Dashboard
- Add Restaurant
- Update Restaurant Details
- Delete Restaurant
- Add Menu Items
- Edit Menu Items
- Delete Menu Items
- View Customer Orders
- Update Order Status
- View Top Selling Items

---

# Tech Stack

## Frontend

- React.js
- React Router
- Redux Toolkit
- Axios
- Tailwind CSS
- React Icons
- Vite

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic

---

# Project Structure

```
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── features/
│   ├── services/
│   ├── layouts/
│   ├── routes/
│   └── utils/
│
backend/
│
├── app/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   ├── database/
│   ├── core/
│   └── main.py
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/foodie
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Run Migrations

```bash
alembic upgrade head
```

### Start Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Install dependencies

```bash
npm install
```

Start development server

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# API Modules

- Authentication
- Customer
- Restaurant
- Restaurant Owner
- Menu
- Cart
- Orders
- Favorites
- Preferences
- Recommendations

---

# Authentication

The application uses JWT Authentication.

After login, the access token is stored and automatically attached to every authenticated API request.

---

# Main Functionalities

### Customer

- Register/Login
- Browse Restaurants
- Search Restaurants
- Filter Restaurants
- View Menus
- Add to Cart
- Place Orders
- Track Orders
- Manage Favorites
- Update Preferences
- View Recommendations

### Restaurant Owner

- Manage Restaurants
- Manage Menu
- View Orders
- Update Order Status
- Dashboard Analytics

---

# Screens

- Login
- Register
- Home
- Restaurant Details
- Cart
- Checkout
- My Orders
- Profile
- Preferences
- Recommendations
- Favorite Restaurants
- Owner Dashboard
- Restaurant Management
- Menu Management
- Orders Management

---

# Future Enhancements

- Payment Gateway Integration
- Live Order Tracking
- Email Notifications
- Push Notifications
- Restaurant Ratings & Reviews
- Coupons & Offers
- Dark Mode
- Image Upload Support
- Admin Panel

---

Frontend:https://justeatfrontend-web-gufcengjc2bmd6ds.canadacentral-01.azurewebsites.net/
Backend:https://justeat-backend.lemongrass-1bd0eb1d.canadacentral.azurecontainerapps.io/docs#/Authentication/login_user_auth_login_post

# Contributors

- Abhishek Singh

---

# License

This project is developed for learning and educational purposes.
