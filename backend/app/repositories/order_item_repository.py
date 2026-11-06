from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


def create_order_item(
    db: Session,
    order_item: OrderItem,
):
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item