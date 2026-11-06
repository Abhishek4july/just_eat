from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant import Restaurant


def create_order(
    db: Session,
    order: Order,
):
    """
    Save a new order to the database.

    Args:
        db: Database session.
        order: Order object to create.

    Returns:
        The newly created order.
    """
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(
    db: Session,
    order_id: int,
):
    """
    Retrieve an order by its ID.

    Args:
        db: Database session.
        order_id: ID of the order.

    Returns:
        The order if found, otherwise None.
    """
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_customer_orders(
    db: Session,
    customer_id: int,
    search: str | None = None,
):
    """
    Retrieve all orders placed by a customer with optional search filtering.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        search: Optional keyword to filter by restaurant name or order status.

    Returns:
        A list of customer orders.
    """
    query = (
        db.query(Order)
        .options(
            selectinload(Order.restaurant),
            selectinload(Order.order_items).selectinload(OrderItem.menu_item),
        )
        .join(Restaurant)
        .filter(
            Order.customer_id == customer_id,
        )
    )

    if search:
        query = query.filter(
            or_(
                Restaurant.name.ilike(f"%{search}%"),
                cast(Order.status, String).ilike(f"%{search}%"),
            )
        )

    return query.all()


def get_restaurant_orders(
    db: Session,
    restaurant_id: int,
):
    """
    Retrieve all orders for a specific restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.

    Returns:
        A list of restaurant orders.
    """
    return (
        db.query(Order)
        .options(
            selectinload(Order.order_items).selectinload(OrderItem.menu_item)
        )
        .filter(Order.restaurant_id == restaurant_id)
        .all()
    )


def save_order(
    db: Session,
    order: Order,
):
    """
    Save changes made to an existing order.

    Args:
        db: Database session.
        order: Order object to update.

    Returns:
        The updated order.
    """
    db.commit()
    db.refresh(order)
    return order