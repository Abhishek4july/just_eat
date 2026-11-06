from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class CartItem(Base):

    __tablename__="cart_items"
    id=Column(Integer,primary_key=True,index=True)

    cart_id=Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    menu_item_id=Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False,
        )
    

    quantity=Column(
        Integer,
        nullable=False,
        default=1,
    )

    cart=relationship(
        "Cart",
        back_populates="items"
    )

    menu_item=relationship(
        "MenuItem",
        back_populates="cart_items"
    )
