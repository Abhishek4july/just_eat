from datetime import datetime,timezone

from sqlalchemy import Column,DateTime,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Restaurant(Base):
    __tablename__="restaurants"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(String)
    address=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)
    owner_id=Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at=Column(
        DateTime,
        default=lambda:datetime.now(timezone.utc),
    )

    owner=relationship(
        "User",
        back_populates="restaurants"
    )
    menu_items = relationship(
    "MenuItem",
    back_populates="restaurant",
    cascade="all, delete-orphan",
)
    
    orders = relationship(
    "Order",
    back_populates="restaurant",
    cascade="all, delete-orphan",
)
    
    favorited_by = relationship(
    "FavoriteRestaurant",
    back_populates="restaurant",
    cascade="all, delete-orphan",
)