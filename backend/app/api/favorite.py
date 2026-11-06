from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.favorite import FavoriteResponse
from app.services.favorite_service import (
    add_to_favorites,
    remove_from_favorites,
    view_favorites,
)

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)


@router.post(
    "/{menu_item_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_favorite(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a menu item to the authenticated user's favorites.

    Args:
        menu_item_id: ID of the menu item to add.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The newly added favorite menu item.
    """
    return add_to_favorites(
        db=db,
        current_user=current_user,
        menu_item_id=menu_item_id,
    )


@router.get(
    "",
    response_model=list[FavoriteResponse],
)
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all favorite menu items of the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of favorite menu items.
    """
    return view_favorites(
        db=db,
        current_user=current_user,
    )


@router.delete(
    "/{menu_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_favorite(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a menu item from the authenticated user's favorites.

    Args:
        menu_item_id: ID of the menu item to remove.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        None.
    """
    remove_from_favorites(
        db=db,
        current_user=current_user,
        menu_item_id=menu_item_id,
    )