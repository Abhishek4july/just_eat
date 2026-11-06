from sqlalchemy.orm import Session

from app.models.favorite_restaurant import FavoriteRestaurant


def get_favorite_restaurant(
    db: Session,
    customer_id: int,
    restaurant_id: int,
):
    """
    Retrieve a favorite restaurant for a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        restaurant_id: ID of the restaurant.

    Returns:
        The favorite restaurant record if it exists, otherwise None.
    """
    return (
        db.query(FavoriteRestaurant)
        .filter(
            FavoriteRestaurant.customer_id == customer_id,
            FavoriteRestaurant.restaurant_id == restaurant_id,
        )
        .first()
    )


def get_favorite_restaurants(
    db: Session,
    customer_id: int,
):
    """
    Retrieve all favorite restaurants of a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        A list of the customer's favorite restaurants.
    """
    return (
        db.query(FavoriteRestaurant)
        .filter(
            FavoriteRestaurant.customer_id == customer_id,
        )
        .all()
    )


def create_favorite_restaurant(
    db: Session,
    customer_id: int,
    restaurant_id: int,
):
    """
    Add a restaurant to a customer's favorites.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        restaurant_id: ID of the restaurant.

    Returns:
        The newly created favorite restaurant record.
    """
    favorite = FavoriteRestaurant(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def delete_favorite_restaurant(
    db: Session,
    favorite: FavoriteRestaurant,
):
    """
    Remove a restaurant from a customer's favorites.

    Args:
        db: Database session.
        favorite: Favorite restaurant record to delete.

    Returns:
        None.
    """
    db.delete(favorite)
    db.commit()