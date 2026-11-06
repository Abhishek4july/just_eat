from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class FavoriteRestaurant(Base):
    __tablename__ = "favorite_restaurants"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

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

    customer = relationship(
        "User",
        back_populates="favorite_restaurants",
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="favorited_by",
    )