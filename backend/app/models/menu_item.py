from sqlalchemy import Boolean
from datetime import datetime,timezone
from sqlalchemy import Column,DateTime,Float,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.restaurant import Restaurant
from sqlalchemy import Boolean

class MenuItem(Base):
    __tablename__="menu_items"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(String)
    price=Column(Float,nullable=False)
    restaurant_id=Column(
        Integer,
        ForeignKey("restaurants.id"),
        nullable=False
    )
    category = Column(String, nullable=False)
    is_special = Column(Boolean, default=False)
    order_count = Column(Integer, default=0)
    created_at=Column(
        DateTime,
        default=lambda:datetime.now(timezone.utc),
    )

    restaurant=relationship(
        "Restaurant",
        back_populates="menu_items",
    )

    order_items = relationship(
    "OrderItem",
    back_populates="menu_item",
)
    
    cart_items = relationship(
    "CartItem",
    back_populates="menu_item",
)
    
    favorites = relationship(
    "Favorite",
    back_populates="menu_item",
)
    
    is_special = Column(
    Boolean,
    default=False,
    nullable=False,
)

    special_title = Column(
        String,
        nullable=True,
    )
    
