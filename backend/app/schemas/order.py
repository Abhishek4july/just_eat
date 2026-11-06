from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.schemas.order_item import OrderItemCreate, OrderItemResponse

# Order response schema for API responses
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: OrderStatus


# Response schema for Order objects
class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    restaurant_name: str | None = None  # Restaurant name is populated from the Order model property
    total_price: float
    status: OrderStatus
    created_at: datetime
    order_items: list[OrderItemResponse]  # List of items in the order

    model_config = ConfigDict(from_attributes=True)