from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.dependencies.roles import require_restaurant_owner
from app.models.user import User
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemResponse,
    MenuItemUpdate,
)
from app.services.menu_service import (
    create_new_menu_item,
    get_restaurant_menu,
    get_menu_item,
    update_menu_item,
    remove_menu_item,
    get_special_items,
)

router = APIRouter(
    tags=["Menu"],
)


@router.post(
    "/restaurant/{restaurant_id}/menu",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_menu(
    restaurant_id: int,
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Create a new menu item for a restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        menu_item: Details of the menu item to create.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        The newly created menu item.
    """
    return create_new_menu_item(
        db=db,
        restaurant_id=restaurant_id,
        menu_item=menu_item,
        current_user=current_user,
    )


@router.get(
    "/restaurant/{restaurant_id}/menu",
    response_model=list[MenuItemResponse],
)
def get_restaurant_menu_endpoint(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all menu items of a restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of menu items.
    """
    return get_restaurant_menu(
        db=db,
        restaurant_id=restaurant_id,
    )


@router.get(
    "/menu/{menu_item_id}",
    response_model=MenuItemResponse,
)
def get_menu_item_endpoint(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve details of a specific menu item.

    Args:
        menu_item_id: ID of the menu item.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The requested menu item.
    """
    return get_menu_item(
        db=db,
        menu_item_id=menu_item_id,
    )


@router.put(
    "/menu/{menu_item_id}",
    response_model=MenuItemResponse,
)
def update_menu_item_endpoint(
    menu_item_id: int,
    menu_item: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Update an existing menu item.

    Args:
        menu_item_id: ID of the menu item.
        menu_item: Updated menu item details.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated menu item.
    """
    return update_menu_item(
        db=db,
        menu_item_id=menu_item_id,
        menu_item_update=menu_item,
        current_user=current_user,
    )


@router.delete("/menu/{menu_item_id}")
def delete_menu_item_endpoint(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Delete a menu item from a restaurant.

    Args:
        menu_item_id: ID of the menu item to delete.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        Success message after deletion.
    """
    remove_menu_item(
        db=db,
        menu_item_id=menu_item_id,
        current_user=current_user,
    )

    return {
        "message": "Menu item deleted successfully."
    }


@router.get(
    "/specials",
    response_model=list[MenuItemResponse],
)
def view_special_items(
    db: Session = Depends(get_db),
):
    """
    Retrieve all menu items marked as specials.

    Args:
        db: Database session.

    Returns:
        A list of special menu items.
    """
    return get_special_items(
        db,
    )