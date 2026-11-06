from sqlalchemy.orm import Session

from app.core.exceptions import (
    FavoriteRestaurantAlreadyExistsException,
    FavoriteRestaurantNotFoundException,
    RestaurantNotFoundException,
)
from app.core.logger import logger
from app.models.user import User
from app.repositories.favorite_restaurant_repository import (
    create_favorite_restaurant,
    delete_favorite_restaurant,
    get_favorite_restaurant,
    get_favorite_restaurants,
)
from app.repositories.restaurant_repository import (
    get_restaurant_by_id,
)


def add_favorite_restaurant(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Add a restaurant to the authenticated user's favorites.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated user.

    Returns:
        The newly created favorite restaurant.

    Raises:
        RestaurantNotFoundException: If the restaurant does not exist.
        FavoriteRestaurantAlreadyExistsException: If the restaurant is already in the user's favorites.
    """
    logger.info(
        "Adding restaurant %d to favorites for user %d.",
        restaurant_id,
        current_user.id,
    )

    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if not restaurant:
        raise RestaurantNotFoundException(
            restaurant_id,
        )

    favorite = get_favorite_restaurant(
        db,
        current_user.id,
        restaurant_id,
    )

    if favorite:
        raise FavoriteRestaurantAlreadyExistsException(
            restaurant_id,
        )

    return create_favorite_restaurant(
        db,
        current_user.id,
        restaurant_id,
    )


def view_favorite_restaurants(
    db: Session,
    current_user: User,
):
    """
    Retrieve all favorite restaurants of the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of the user's favorite restaurants.
    """
    logger.info(
        "Fetching favorite restaurants for user %d.",
        current_user.id,
    )

    return get_favorite_restaurants(
        db,
        current_user.id,
    )


def remove_favorite_restaurant(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Remove a restaurant from the authenticated user's favorites.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated user.

    Returns:
        A confirmation message.

    Raises:
        FavoriteRestaurantNotFoundException: If the restaurant is not in the user's favorites.
    """
    logger.info(
        "Removing restaurant %d from favorites for user %d.",
        restaurant_id,
        current_user.id,
    )

    favorite = get_favorite_restaurant(
        db,
        current_user.id,
        restaurant_id,
    )

    if not favorite:
        raise FavoriteRestaurantNotFoundException(
            restaurant_id,
        )

    delete_favorite_restaurant(
        db,
        favorite,
    )

    return {
        "message": "Restaurant removed from favorites."
    }