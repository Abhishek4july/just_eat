from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False,
    )

    status = Column(
        SqlEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
    )

    total_price = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    customer = relationship(
        "User",
        back_populates="orders",
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="orders",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    # Property to get restaurant name from the related restaurant object
    # Used for API responses to display restaurant name alongside restaurant_id
    @property
    def restaurant_name(self):
        return self.restaurant.name if self.restaurant else None