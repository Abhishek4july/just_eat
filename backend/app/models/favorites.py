from sqlalchemy import Column,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from app.db.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id", ondelete="CASCADE"),
        nullable=False,
    )

    customer = relationship(
        "User",
        back_populates="favorites",
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="favorites",
    )