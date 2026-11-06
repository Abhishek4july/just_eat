from fastapi import FastAPI
from app.db.database import engine
from app.api.auth import router as auth_router
from fastapi.exceptions import HTTPException
from app.core.exception_handler import http_exception_handler
from app.api.restaurants import router as restaurant_router
from app.api.menu import router as menu_router
from app.models.order import Order
from fastapi.middleware.cors import CORSMiddleware
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.api.order import router as order_router
from app.api.recommendation import router as recommendation_router
from app.api import cart
from app.api.favorite_restaurant import (
    router as favorite_restaurant_router,
)
from app.api.preference import router as preference_router
from app.api.favorite import router as favorite_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.include_router(
    preference_router,
)
app.include_router(
    recommendation_router,
)
app.include_router(
    favorite_restaurant_router,
)
app.include_router(
    favorite_router,
)
app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(restaurant_router)
app.include_router(order_router)
app.include_router(cart.router)
@app.get("/")
def home():
    return {"message": "JustEat Backend Running"}