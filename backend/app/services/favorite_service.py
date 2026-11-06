from sqlalchemy.orm import Session

from app.core.exceptions import (
    FavoriteAlreadyExistsException,
    FavoriteNotFoundException,
    MenuItemNotFoundException,
)
from app.core.logger import logger
from app.models.user import User
from app.repositories.favorite_repository import (
    create_favorite,
    delete_favorite,
    get_favorite,
    get_favorites_by_customer,
)
from app.repositories.menu_repository import get_menu_item_by_id


def add_to_favorites(
    db: Session,
    current_user: User,
    menu_item_id: int,
):
    """
    Add a menu item to the authenticated user's favorites.

    Args:
        db: Database session.
        current_user: Authenticated user.
        menu_item_id: ID of the menu item.

    Returns:
        The newly created favorite.

    Raises:
        MenuItemNotFoundException: If the menu item does not exist.
        FavoriteAlreadyExistsException: If the menu item is already in the user's favorites.
    """
    logger.info(
        "User %d is adding menu item %d to favorites.",
        current_user.id,
        menu_item_id,
    )

    menu_item = get_menu_item_by_id(
        db,
        menu_item_id,
    )

    if menu_item is None:
        logger.warning(
            "Menu item %d not found.",
            menu_item_id,
        )
        raise MenuItemNotFoundException(menu_item_id)

    favorite = get_favorite(
        db,
        current_user.id,
        menu_item_id,
    )

    if favorite:
        logger.warning(
            "Menu item %d already exists in favorites for user %d.",
            menu_item_id,
            current_user.id,
        )
        raise FavoriteAlreadyExistsException(menu_item_id)

    logger.info(
        "Creating favorite for user %d.",
        current_user.id,
    )

    return create_favorite(
        db,
        current_user.id,
        menu_item_id,
    )


def view_favorites(
    db: Session,
    current_user: User,
):
    """
    Retrieve all favorite menu items of the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of the user's favorite menu items.
    """
    logger.info(
        "Fetching favorites for user %d.",
        current_user.id,
    )

    return get_favorites_by_customer(
        db,
        current_user.id,
    )


def remove_from_favorites(
    db: Session,
    current_user: User,
    menu_item_id: int,
):
    """
    Remove a menu item from the authenticated user's favorites.

    Args:
        db: Database session.
        current_user: Authenticated user.
        menu_item_id: ID of the menu item.

    Returns:
        None.

    Raises:
        FavoriteNotFoundException: If the menu item is not in the user's favorites.
    """
    logger.info(
        "User %d is removing menu item %d from favorites.",
        current_user.id,
        menu_item_id,
    )

    favorite = get_favorite(
        db,
        current_user.id,
        menu_item_id,
    )

    if favorite is None:
        logger.warning(
            "Menu item %d not found in favorites for user %d.",
            menu_item_id,
            current_user.id,
        )
        raise FavoriteNotFoundException(menu_item_id)

    delete_favorite(
        db,
        favorite,
    )

    logger.info(
        "Menu item %d removed from favorites for user %d.",
        menu_item_id,
        current_user.id,
    )