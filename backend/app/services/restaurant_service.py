from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    RestaurantAlreadyExistsException,
    RestaurantNotFoundException,
    UnauthorizedException,
)
from app.core.logger import logger
from app.models.user import User
from app.repositories.menu_repository import get_top_selling_items
from app.repositories.restaurant_repository import (
    create_restaurant,
    delete_restaurant,
    get_all_restaurants,
    get_restaurant_by_id,
    get_restaurant_by_name,
    get_restaurant_dashboard,
    save_restaurant,
)
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
)


def create_new_restaurant(
    db: Session,
    restaurant: RestaurantCreate,
    current_user: User,
):
    """
    Create a new restaurant for the authenticated restaurant owner.

    Args:
        db: Database session.
        restaurant: Restaurant details.
        current_user: Authenticated user.

    Returns:
        The newly created restaurant.

    Raises:
        UnauthorizedException: If the user is not a restaurant owner.
        RestaurantAlreadyExistsException: If a restaurant with the same name already exists.
    """
    if current_user.role != "RESTAURANT_OWNER":
        logger.warning(
            "Unauthorized restaurant creation attempt by %s",
            current_user.email,
        )
        raise UnauthorizedException()

    logger.info(
        "Creating restaurant '%s' for owner %s",
        restaurant.name,
        current_user.email,
    )

    existing = get_restaurant_by_name(
        db,
        restaurant.name,
    )

    if existing:
        logger.warning(
            "Restaurant '%s' already exists.",
            restaurant.name,
        )
        raise RestaurantAlreadyExistsException()

    db_restaurant = create_restaurant(
        db=db,
        restaurant=restaurant,
        owner_id=current_user.id,
    )

    logger.info(
        "Restaurant '%s' created successfully.",
        db_restaurant.name,
    )

    return db_restaurant


def get_restaurants(
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
        location: Restaurant location filter.
        cuisine: Cuisine type filter.
        min_price: Minimum average price filter.
        max_price: Maximum average price filter.

    Returns:
        A list of matching restaurants.
    """
    logger.info(
        "Fetching restaurants with filters: "
        "name=%s, location=%s, cuisine=%s, min_price=%s, max_price=%s",
        name,
        location,
        cuisine,
        min_price,
        max_price,
    )

    restaurants = get_all_restaurants(
        db=db,
        name=name,
        location=location,
        cuisine=cuisine,
        min_price=min_price,
        max_price=max_price,
    )

    logger.info(
        "Found %d restaurants.",
        len(restaurants),
    )

    return restaurants


def get_restaurant(
    db: Session,
    restaurant_id: int,
):
    """
    Retrieve a restaurant by its ID.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.

    Returns:
        The requested restaurant.

    Raises:
        RestaurantNotFoundException: If the restaurant does not exist.
    """
    logger.info(
        "Fetching restaurant with id=%d",
        restaurant_id,
    )

    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if restaurant is None:
        logger.warning(
            "Restaurant %d not found",
            restaurant_id,
        )
        raise RestaurantNotFoundException()

    return restaurant


def update_restaurant(
    db: Session,
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    current_user: User,
):
    """
    Update an existing restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        restaurant_data: Updated restaurant details.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated restaurant.

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
        logger.warning(
            "User %s attempted to update restaurant %d owned by user %d",
            current_user.email,
            restaurant.id,
            restaurant.owner_id,
        )
        raise UnauthorizedException()

    if restaurant_data.name is not None:
        restaurant.name = restaurant_data.name

    if restaurant_data.description is not None:
        restaurant.description = restaurant_data.description

    if restaurant_data.address is not None:
        restaurant.address = restaurant_data.address

    if restaurant_data.phone is not None:
        restaurant.phone = restaurant_data.phone

    if restaurant_data.city is not None:
        restaurant.city = restaurant_data.city

    if restaurant_data.state is not None:
        restaurant.state = restaurant_data.state

    if restaurant_data.cuisine is not None:
        restaurant.cuisine = restaurant_data.cuisine

    logger.info(
        "Updating restaurant %d",
        restaurant.id,
    )

    return save_restaurant(
        db,
        restaurant,
    )


def remove_restaurant(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Delete a restaurant owned by the authenticated user.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated restaurant owner.

    Returns:
        None.

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
        logger.warning(
            "User %s attempted to delete restaurant %d",
            current_user.email,
            restaurant.id,
        )
        raise UnauthorizedException()

    logger.info(
        "Deleting restaurant %d",
        restaurant.id,
    )

    delete_restaurant(
        db,
        restaurant,
    )

    logger.info(
        "Restaurant %d deleted successfully",
        restaurant.id,
    )


def get_dashboard(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Retrieve dashboard statistics for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated restaurant owner.

    Returns:
        Dashboard statistics for the restaurant.

    Raises:
        HTTPException: If the user is not authorized or the restaurant does not exist.
    """
    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this dashboard",
        )

    dashboard = get_restaurant_dashboard(
        db,
        restaurant_id,
    )

    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return dashboard


def get_top_items(
    db: Session,
    restaurant_id: int,
    current_user: User,
):
    """
    Retrieve the top-selling menu items for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        current_user: Authenticated restaurant owner.

    Returns:
        A list of top-selling menu items.

    Raises:
        HTTPException: If the restaurant does not exist or the user is not authorized.
    """
    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    if restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    return get_top_selling_items(
        db,
        restaurant_id,
    )