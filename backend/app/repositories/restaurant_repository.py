from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.models.order import Order, OrderStatus
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate


def create_restaurant(
    db: Session,
    restaurant: RestaurantCreate,
    owner_id: int,
):
    """
    Create a new restaurant.

    Args:
        db: Database session.
        restaurant: Restaurant details.
        owner_id: ID of the restaurant owner.

    Returns:
        The newly created restaurant.
    """
    db_restaurant = Restaurant(
        name=restaurant.name,
        description=restaurant.description,
        address=restaurant.address,
        city=restaurant.city,
        state=restaurant.state,
        cuisine=restaurant.cuisine,
        phone=restaurant.phone,
        owner_id=owner_id,
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def get_restaurant_by_id(
    db: Session,
    restaurant_id: int,
):
    """
    Retrieve a restaurant by its ID.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.

    Returns:
        The restaurant if found, otherwise None.
    """
    return (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id)
        .first()
    )


def get_my_restaurants(
    db: Session,
    owner_id: int,
):
    """
    Retrieve all restaurants owned by a specific user.

    Args:
        db: Database session.
        owner_id: ID of the restaurant owner.

    Returns:
        A list of restaurants owned by the user.
    """
    return (
        db.query(Restaurant)
        .filter(Restaurant.owner_id == owner_id)
        .all()
    )


def get_all_restaurants(
    db: Session,
    name: str | None = None,
    location: str | None = None,
    cuisine: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
):
    """
    Retrieve restaurants with optional filters.

    Args:
        db: Database session.
        name: Restaurant name filter.
        location: City filter.
        cuisine: Cuisine filter.
        min_price: Minimum menu item price.
        max_price: Maximum menu item price.

    Returns:
        A list of restaurants matching the filters.
    """
    query = db.query(Restaurant)

    if min_price is not None or max_price is not None:
        query = query.join(MenuItem)

    if name:
        query = query.filter(
            Restaurant.name.ilike(f"%{name}%")
        )

    if location:
        query = query.filter(
            Restaurant.city.ilike(f"%{location}%")
        )

    if cuisine:
        query = query.filter(
            Restaurant.cuisine.ilike(f"%{cuisine}%")
        )

    if min_price is not None:
        query = query.filter(
            MenuItem.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            MenuItem.price <= max_price
        )

    return query.distinct().all()


def delete_restaurant(
    db: Session,
    restaurant: Restaurant,
):
    """
    Delete a restaurant.

    Args:
        db: Database session.
        restaurant: Restaurant to delete.

    Returns:
        None.
    """
    db.delete(restaurant)
    db.commit()


def save_restaurant(
    db: Session,
    restaurant: Restaurant,
):
    """
    Save changes made to a restaurant.

    Args:
        db: Database session.
        restaurant: Restaurant to update.

    Returns:
        The updated restaurant.
    """
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurant_by_name(
    db: Session,
    name: str,
):
    """
    Retrieve a restaurant by its name.

    Args:
        db: Database session.
        name: Restaurant name.

    Returns:
        The restaurant if found, otherwise None.
    """
    return (
        db.query(Restaurant)
        .filter(Restaurant.name == name)
        .first()
    )


def get_restaurant_dashboard(
    db: Session,
    restaurant_id: int,
):
    """
    Retrieve dashboard statistics for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.

    Returns:
        A dictionary containing order statistics and total revenue,
        or None if the restaurant does not exist.
    """
    restaurant = get_restaurant_by_id(db, restaurant_id)

    if not restaurant:
        return None

    total_orders = (
        db.query(func.count(Order.id))
        .filter(Order.restaurant_id == restaurant_id)
        .scalar()
    )

    pending_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.PENDING,
        )
        .scalar()
    )

    confirmed_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.CONFIRMED,
        )
        .scalar()
    )

    preparing_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.PREPARING,
        )
        .scalar()
    )

    ready_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.READY,
        )
        .scalar()
    )

    delivered_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.DELIVERED,
        )
        .scalar()
    )

    cancelled_orders = (
        db.query(func.count(Order.id))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.CANCELLED,
        )
        .scalar()
    )

    total_revenue = (
        db.query(func.sum(Order.total_price))
        .filter(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.DELIVERED,
        )
        .scalar()
        or 0
    )

    return {
        "restaurant_id": restaurant.id,
        "restaurant_name": restaurant.name,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "preparing_orders": preparing_orders,
        "ready_orders": ready_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": total_revenue,
    }