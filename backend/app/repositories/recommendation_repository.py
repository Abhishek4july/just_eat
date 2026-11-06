from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.preference import Preference
from app.models.restaurant import Restaurant


def get_user_preference(
    db: Session,
    customer_id: int,
):
    """
    Retrieve the food preferences of a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        The customer's preference if found, otherwise None.
    """
    return (
        db.query(Preference)
        .filter(
            Preference.customer_id == customer_id,
        )
        .first()
    )


def get_restaurants_by_cuisine(
    db: Session,
    cuisine: str,
):
    """
    Retrieve restaurants that serve a specific cuisine.

    Args:
        db: Database session.
        cuisine: Cuisine type to search for.

    Returns:
        A list of restaurants matching the cuisine.
    """
    return (
        db.query(Restaurant)
        .filter(
            Restaurant.cuisine == cuisine,
        )
        .all()
    )


def get_user_favorite_restaurant(
    db: Session,
    customer_id: int,
):
    """
    Retrieve the customer's most frequently ordered restaurant.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        The restaurant ID and order count of the customer's favorite restaurant,
        or None if no orders exist.
    """
    return (
        db.query(
            Order.restaurant_id,
            func.count(Order.id).label("count"),
        )
        .filter(
            Order.customer_id == customer_id,
        )
        .group_by(
            Order.restaurant_id,
        )
        .order_by(
            desc("count"),
        )
        .first()
    )


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
        .filter(
            Restaurant.id == restaurant_id,
        )
        .first()
    )


def get_popular_restaurants(
    db: Session,
):
    """
    Retrieve the most popular restaurants based on order count.

    Args:
        db: Database session.

    Returns:
        A list of the top 10 most popular restaurants.
    """
    return (
        db.query(Restaurant)
        .join(Order)
        .group_by(Restaurant.id)
        .order_by(desc(func.count(Order.id)))
        .limit(10)
        .all()
    )