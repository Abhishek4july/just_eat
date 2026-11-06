from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import (
    MenuItemNotFoundException,
    RestaurantNotFoundException,
    UnauthorizedException,
)
from app.core.logger import logger
from app.models.user import User
from app.repositories.menu_repository import (
    create_menu_item,
    delete_menu_item,
    get_menu_item_by_id,
    get_menu_items_by_restaurant,
    get_special_menu_items,
    save_menu_item,
)
from app.repositories.restaurant_repository import get_restaurant_by_id
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemUpdate,
)


def create_new_menu_item(
    db: Session,
    restaurant_id: int,
    menu_item: MenuItemCreate,
    current_user: User,
):
    """
    Create a new menu item for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        menu_item: Details of the menu item to create.
        current_user: Authenticated restaurant owner.

    Returns:
        The newly created menu item.

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
            "User %s attempted to add menu item to restaurant %d",
            current_user.email,
            restaurant.id,
        )
        raise UnauthorizedException()

    logger.info(
        "Creating menu item '%s' for restaurant %d",
        menu_item.name,
        restaurant.id,
    )

    db_menu_item = create_menu_item(
        db=db,
        menu_item=menu_item,
        restaurant_id=restaurant.id,
    )

    logger.info(
        "Menu item '%s' created successfully",
        db_menu_item.name,
    )

    return db_menu_item


def get_restaurant_menu(
    db: Session,
    restaurant_id: int,
):
    """
    Retrieve all menu items for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.

    Returns:
        A list of menu items.

    Raises:
        RestaurantNotFoundException: If the restaurant does not exist.
    """
    restaurant = get_restaurant_by_id(
        db,
        restaurant_id,
    )

    if restaurant is None:
        logger.warning(
            "Restaurant with ID %d not found.",
            restaurant_id,
        )
        raise RestaurantNotFoundException()

    logger.info(
        "Fetching menu for restaurant ID %d",
        restaurant_id,
    )

    return get_menu_items_by_restaurant(
        db=db,
        restaurant_id=restaurant_id,
    )


def get_menu_item(
    db: Session,
    menu_item_id: int,
):
    """
    Retrieve a menu item by its ID.

    Args:
        db: Database session.
        menu_item_id: ID of the menu item.

    Returns:
        The requested menu item.

    Raises:
        MenuItemNotFoundException: If the menu item does not exist.
    """
    menu_item = get_menu_item_by_id(
        db,
        menu_item_id,
    )

    if menu_item is None:
        logger.warning(
            "Menu item with ID %d not found.",
            menu_item_id,
        )
        raise MenuItemNotFoundException()

    logger.info(
        "Fetched menu item ID %d",
        menu_item_id,
    )

    return menu_item


def update_menu_item(
    db: Session,
    menu_item_id: int,
    menu_item_update: MenuItemUpdate,
    current_user: User,
):
    """
    Update an existing menu item.

    Args:
        db: Database session.
        menu_item_id: ID of the menu item.
        menu_item_update: Updated menu item details.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated menu item.

    Raises:
        MenuItemNotFoundException: If the menu item does not exist.
        UnauthorizedException: If the user does not own the restaurant.
    """
    menu_item = get_menu_item_by_id(
        db,
        menu_item_id,
    )

    if menu_item is None:
        logger.warning(
            "Menu item with ID %d not found.",
            menu_item_id,
        )
        raise MenuItemNotFoundException()

    if menu_item.restaurant.owner_id != current_user.id:
        logger.warning(
            "User %d attempted to update menu item %d.",
            current_user.id,
            menu_item_id,
        )
        raise UnauthorizedException()

    if menu_item_update.name is not None:
        menu_item.name = menu_item_update.name

    if menu_item_update.description is not None:
        menu_item.description = menu_item_update.description

    if menu_item_update.price is not None:
        menu_item.price = menu_item_update.price

    if menu_item_update.category is not None:
        menu_item.category = menu_item_update.category

    if menu_item_update.is_special is not None:
        menu_item.is_special = menu_item_update.is_special

    if not menu_item_update.is_special:
        menu_item.special_title = None

    if menu_item_update.special_title is not None:
        menu_item.special_title = menu_item_update.special_title

    logger.info(
        "Menu item %d updated successfully.",
        menu_item_id,
    )

    return save_menu_item(
        db,
        menu_item,
    )


def remove_menu_item(
    db: Session,
    menu_item_id: int,
    current_user: User,
):
    """
    Delete a menu item from a restaurant.

    Args:
        db: Database session.
        menu_item_id: ID of the menu item.
        current_user: Authenticated restaurant owner.

    Returns:
        None.

    Raises:
        MenuItemNotFoundException: If the menu item does not exist.
        UnauthorizedException: If the user does not own the restaurant.
        HTTPException: If the menu item has already been ordered.
    """
    menu_item = get_menu_item_by_id(
        db,
        menu_item_id,
    )

    if menu_item is None:
        logger.warning(
            "Menu item with ID %d not found.",
            menu_item_id,
        )
        raise MenuItemNotFoundException()

    if menu_item.restaurant.owner_id != current_user.id:
        logger.warning(
            "User %d attempted to delete menu item %d.",
            current_user.id,
            menu_item_id,
        )
        raise UnauthorizedException()

    if menu_item.order_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This menu item has already been ordered and cannot be deleted.",
        )

    delete_menu_item(
        db,
        menu_item,
    )

    logger.info(
        "Menu item %d deleted successfully.",
        menu_item_id,
    )


def get_special_items(
    db: Session,
):
    """
    Retrieve all menu items marked as specials.

    Args:
        db: Database session.

    Returns:
        A list of special menu items.
    """
    logger.info(
        "Fetching special menu items."
    )

    return get_special_menu_items(
        db,
    )