from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate


def create_menu_item(
    db: Session,
    menu_item: MenuItemCreate,
    restaurant_id: int,
):
    """
    Create a new menu item for a restaurant.

    Args:
        db: Database session.
        menu_item: Details of the menu item to create.
        restaurant_id: ID of the restaurant.

    Returns:
        The newly created menu item.
    """
    db_menu_item = MenuItem(
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        category=menu_item.category,
        restaurant_id=restaurant_id,
        is_special=menu_item.is_special,
        special_title=menu_item.special_title,
    )

    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)

    return db_menu_item


def get_menu_item_by_id(
    db: Session,
    menu_item_id: int,
):
    """
    Retrieve a menu item by its ID.

    Args:
        db: Database session.
        menu_item_id: ID of the menu item.

    Returns:
        The menu item if found, otherwise None.
    """
    return (
        db.query(MenuItem)
        .filter(MenuItem.id == menu_item_id)
        .first()
    )


def get_menu_items_by_restaurant(
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
    """
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .all()
    )


def get_top_selling_items(
    db: Session,
    restaurant_id: int,
    limit: int = 5,
):
    """
    Retrieve the top-selling menu items for a restaurant.

    Args:
        db: Database session.
        restaurant_id: ID of the restaurant.
        limit: Maximum number of menu items to return.

    Returns:
        A list of top-selling menu items.
    """
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .order_by(MenuItem.order_count.desc())
        .limit(limit)
        .all()
    )


def save_menu_item(
    db: Session,
    menu_item: MenuItem,
):
    """
    Save changes made to a menu item.

    Args:
        db: Database session.
        menu_item: Menu item to update.

    Returns:
        The updated menu item.
    """
    db.commit()
    db.refresh(menu_item)
    return menu_item


def delete_menu_item(
    db: Session,
    menu_item: MenuItem,
):
    """
    Delete a menu item.

    Args:
        db: Database session.
        menu_item: Menu item to delete.

    Returns:
        None.
    """
    db.delete(menu_item)
    db.commit()


def get_special_menu_items(
    db: Session,
):
    """
    Retrieve all menu items marked as specials.

    Args:
        db: Database session.

    Returns:
        A list of special menu items.
    """
    return (
        db.query(MenuItem)
        .filter(
            MenuItem.is_special == True,
            MenuItem.special_title.isnot(None),
        )
        .all()
    )