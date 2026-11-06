from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    RestaurantNotFoundException,
    UnauthorizedException,
)
from app.core.logger import logger
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.user import User
from app.repositories.menu_repository import (
    get_menu_item_by_id,
    get_special_menu_items,
)
from app.repositories.order_repository import (
    get_customer_orders,
    get_order_by_id,
    get_restaurant_orders,
    save_order,
)
from app.repositories.restaurant_repository import get_restaurant_by_id
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
)


def create_new_order(
    db: Session,
    order_data: OrderCreate,
    current_user: User,
):
    """
    Create a new order for the authenticated user.

    Args:
        db: Database session.
        order_data: Order details including restaurant and menu items.
        current_user: Authenticated user.

    Returns:
        The newly created order.

    Raises:
        RestaurantNotFoundException: If the restaurant does not exist.
    """
    restaurant = get_restaurant_by_id(
        db,
        order_data.restaurant_id,
    )

    if restaurant is None:
        raise RestaurantNotFoundException()

    total_price = 0

    order = Order(
        customer_id=current_user.id,
        restaurant_id=restaurant.id,
        total_price=0,
    )

    db.add(order)
    db.flush()

    for item in order_data.items:
        menu_item = get_menu_item_by_id(
            db,
            item.menu_item_id,
        )

        if menu_item is None:
            continue

        if menu_item.restaurant_id != restaurant.id:
            continue

        menu_item.order_count += item.quantity

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            price=menu_item.price,
        )

        db.add(order_item)

        total_price += menu_item.price * item.quantity

    order.total_price = total_price

    db.commit()
    db.refresh(order)

    logger.info(
        "Order %d created successfully.",
        order.id,
    )

    return order


def get_my_orders(
    db: Session,
    current_user: User,
    search: str | None = None,
):
    """
    Retrieve all orders placed by the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.
        search: Optional keyword to filter orders.

    Returns:
        A list of the user's orders.
    """
    return get_customer_orders(
        db,
        current_user.id,
        search,
    )


def get_restaurant_order_list(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Retrieve all orders for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated restaurant owner.

    Returns:
        A list of restaurant orders.

    Raises:
        RestaurantNotFoundException: If the restaurant does not exist.
        UnauthorizedException: If the user does not own the restaurant.
    """
    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if restaurant is None:
        raise RestaurantNotFoundException()

    if restaurant.owner_id != current_user.id:
        raise UnauthorizedException()

    return get_restaurant_orders(
        db,
        restaurant_id,
    )


def update_order_status(
    db: Session,
    order_id: int,
    order_update: OrderUpdate,
    current_user: User,
):
    """
    Update the status of an existing order.

    Args:
        db: Database session.
        order_id: ID of the order.
        order_update: Updated order status.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated order.

    Raises:
        RestaurantNotFoundException: If the order does not exist.
        UnauthorizedException: If the user does not own the restaurant.
    """
    order = get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        raise RestaurantNotFoundException()

    if order.restaurant.owner_id != current_user.id:
        raise UnauthorizedException()

    order.status = order_update.status

    return save_order(
        db,
        order,
    )


def cancel_order(
    db: Session,
    order_id: int,
    current_user: User,
):
    """
    Cancel an order placed by the authenticated user.

    Orders can only be cancelled while they are in the
    PENDING or CONFIRMED state.

    Args:
        db: Database session.
        order_id: ID of the order.
        current_user: Authenticated user.

    Returns:
        The cancelled order.

    Raises:
        HTTPException: If the order does not exist, does not belong
        to the user, or cannot be cancelled.
    """
    logger.info(
        "User %d requested cancellation for order %d.",
        current_user.id,
        order_id,
    )

    order = get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        logger.warning(
            "Order %d not found.",
            order_id,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    if order.customer_id != current_user.id:
        logger.warning(
            "User %d attempted to cancel order %d owned by user %d.",
            current_user.id,
            order_id,
            order.customer_id,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to cancel this order.",
        )

    if order.status not in [
        OrderStatus.PENDING,
        OrderStatus.CONFIRMED,
    ]:
        logger.warning(
            "Cancellation rejected for order %d. Current status: %s",
            order.id,
            order.status,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled.",
        )

    order.status = OrderStatus.CANCELLED

    order = save_order(
        db,
        order,
    )

    logger.info(
        "Order %d cancelled successfully by user %d.",
        order.id,
        current_user.id,
    )

    return order


def get_special_items(
    db: Session,
):
    """
    Retrieve all menu items marked as specials.

    Args:
        db: Database session.

    Returns:
        A list of special menu items.
    """
    logger.info(
        "Fetching special menu items."
    )

    return get_special_menu_items(
        db,
    )