from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    favorite_cuisine = Column(
        String,
        nullable=True,
    )

    dietary_restriction = Column(
        String,
        nullable=True,
    )

    customer = relationship(
        "User",
        back_populates="preference",
    )