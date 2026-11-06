from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_restaurant_owner
from app.models.user import User
from app.repositories.restaurant_repository import (
    delete_restaurant,
    get_my_restaurants,
)
from app.schemas.dashboard import DashboardResponse
from app.schemas.menu_dashboard import TopMenuItemResponse
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant_service import (
    create_new_restaurant,
    get_dashboard,
    get_restaurant,
    get_restaurants as get_restaurants_service,
    get_top_items,
    update_restaurant,
)

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"],
)


@router.get(
    "/my",
    response_model=list[RestaurantResponse],
)
def my_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Retrieve all restaurants owned by the authenticated restaurant owner.

    Args:
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        A list of restaurants owned by the user.
    """
    return get_my_restaurants(
        db=db,
        owner_id=current_user.id,
    )


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Create a new restaurant.

    Args:
        restaurant: Restaurant details.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        The newly created restaurant.
    """
    return create_new_restaurant(
        db=db,
        restaurant=restaurant,
        current_user=current_user,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def get_restaurant_by_id(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve details of a specific restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The requested restaurant.
    """
    return get_restaurant(
        db=db,
        restaurant_id=restaurant_id,
    )


@router.get(
    "/",
    response_model=list[RestaurantResponse],
)
def get_restaurants(
    name: Optional[str] = None,
    location: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve restaurants with optional filtering.

    Args:
        name: Restaurant name filter.
        location: Restaurant location filter.
        cuisine: Cuisine type filter.
        min_price: Minimum average price filter.
        max_price: Maximum average price filter.
        db: Database session.

    Returns:
        A list of restaurants matching the filters.
    """
    return get_restaurants_service(
        db=db,
        name=name,
        location=location,
        cuisine=cuisine,
        min_price=min_price,
        max_price=max_price,
    )


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
)
def update_restaurant_api(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Update an existing restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        restaurant: Updated restaurant details.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated restaurant.
    """
    return update_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        restaurant_data=restaurant,
        current_user=current_user,
    )


@router.get(
    "/{restaurant_id}/dashboard",
    response_model=DashboardResponse,
)
def restaurant_dashboard(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Retrieve dashboard statistics for a restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        Dashboard summary containing restaurant metrics.
    """
    return get_dashboard(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
    )


@router.get(
    "/{restaurant_id}/top-items",
    response_model=list[TopMenuItemResponse],
)
def top_selling_items(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Retrieve the top-selling menu items for a restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        A list of top-selling menu items.
    """
    return get_top_items(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
    )