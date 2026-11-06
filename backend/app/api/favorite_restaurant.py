from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.favorite_restaurant import (
    FavoriteRestaurantResponse,
)
from app.services.favorite_restaurant_service import (
    add_favorite_restaurant,
    remove_favorite_restaurant,
    view_favorite_restaurants,
)

router = APIRouter(
    prefix="/favorite-restaurants",
    tags=["Favorite Restaurants"],
)


@router.post(
    "/{restaurant_id}",
    response_model=FavoriteRestaurantResponse,
)
def add_restaurant_to_favorites(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a restaurant to the authenticated user's favorites.

    Args:
        restaurant_id: ID of the restaurant to add.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The newly added favorite restaurant.
    """
    return add_favorite_restaurant(
        db,
        restaurant_id,
        current_user,
    )


@router.get(
    "",
    response_model=List[FavoriteRestaurantResponse],
)
def get_favorite_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all favorite restaurants of the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of favorite restaurants.
    """
    return view_favorite_restaurants(
        db,
        current_user,
    )


@router.delete(
    "/{restaurant_id}",
)
def delete_favorite_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a restaurant from the authenticated user's favorites.

    Args:
        restaurant_id: ID of the restaurant to remove.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Confirmation of successful removal.
    """
    return remove_favorite_restaurant(
        db,
        restaurant_id,
        current_user,
    )