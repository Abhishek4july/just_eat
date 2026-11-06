from sqlalchemy import Column,Integer,String
from app.db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    role=Column(String,nullable=False)
    restaurants = relationship(
    "Restaurant",
    back_populates="owner",
    cascade="all, delete-orphan",
)
    orders = relationship(
    "Order",
    back_populates="customer",
    cascade="all, delete-orphan",
)
    
    cart = relationship(
    "Cart",
    back_populates="customer",
    uselist=False
)
    
    favorites = relationship(
    "Favorite",
    back_populates="customer",
    cascade="all, delete-orphan",
)
    

    preference = relationship(
    "Preference",
    back_populates="customer",
    uselist=False,
    cascade="all, delete-orphan",
)
    

    favorite_restaurants = relationship(
    "FavoriteRestaurant",
    back_populates="customer",
    cascade="all, delete-orphan",
)