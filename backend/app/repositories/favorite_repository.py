from sqlalchemy.orm import Session

from app.models.favorites import Favorite


def get_favorite(
    db: Session,
    customer_id: int,
    menu_item_id: int,
):
    """
    Retrieve a favorite menu item for a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        menu_item_id: ID of the menu item.

    Returns:
        The favorite record if it exists, otherwise None.
    """
    return (
        db.query(Favorite)
        .filter(
            Favorite.customer_id == customer_id,
            Favorite.menu_item_id == menu_item_id,
        )
        .first()
    )


def get_favorites_by_customer(
    db: Session,
    customer_id: int,
):
    """
    Retrieve all favorite menu items of a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        A list of the customer's favorite menu items.
    """
    return (
        db.query(Favorite)
        .filter(
            Favorite.customer_id == customer_id,
        )
        .all()
    )


def create_favorite(
    db: Session,
    customer_id: int,
    menu_item_id: int,
):
    """
    Add a menu item to a customer's favorites.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        menu_item_id: ID of the menu item.

    Returns:
        The newly created favorite record.
    """
    favorite = Favorite(
        customer_id=customer_id,
        menu_item_id=menu_item_id,
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def delete_favorite(
    db: Session,
    favorite: Favorite,
):
    """
    Remove a menu item from a customer's favorites.

    Args:
        db: Database session.
        favorite: Favorite record to delete.

    Returns:
        None.
    """
    db.delete(favorite)
    db.commit()