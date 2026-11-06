from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.models.order import Order
from app.models.order_item import OrderItem

from sqlalchemy.orm import configure_mappers

configure_mappers()

print("All mappers configured successfully")