from sqlalchemy.orm import Session

from app.core.exceptions import (
    MenuItemNotFoundException,
)
from app.core.logger import logger
from app.models.user import User
from app.repositories.cart_repository import (
    clear_cart,
    create_cart,
    create_cart_item,
    delete_cart_item,
    get_cart_by_customer,
    get_cart_item,
    get_cart_items,
    save_cart_item,
)
from app.repositories.menu_repository import (
    get_menu_item_by_id,
)


def add_to_cart(
    db: Session,
    current_user: User,
    menu_item_id: int,
    quantity: int,
):
    """
    Add a menu item to the authenticated user's cart.

    If the item already exists in the cart, its quantity is increased.

    Args:
        db: Database session.
        current_user: Authenticated user.
        menu_item_id: ID of the menu item.
        quantity: Quantity to add.

    Returns:
        The created or updated cart item.

    Raises:
        MenuItemNotFoundException: If the menu item does not exist.
    """
    menu_item = get_menu_item_by_id(
        db,
        menu_item_id,
    )

    if menu_item is None:
        logger.warning(
            "Menu item %d not found.",
            menu_item_id,
        )
        raise MenuItemNotFoundException()

    cart = get_cart_by_customer(
        db,
        current_user.id,
    )

    if cart is None:
        logger.info(
            "Creating cart for user %d",
            current_user.id,
        )

        cart = create_cart(
            db,
            current_user.id,
        )

    cart_item = get_cart_item(
        db,
        cart.id,
        menu_item_id,
    )

    if cart_item:
        cart_item.quantity += quantity

        logger.info(
            "Updated quantity for menu item %d",
            menu_item_id,
        )

        return save_cart_item(
            db,
            cart_item,
        )

    logger.info(
        "Adding menu item %d to cart",
        menu_item_id,
    )

    return create_cart_item(
        db=db,
        cart_id=cart.id,
        menu_item_id=menu_item_id,
        quantity=quantity,
    )


def get_user_cart(
    db: Session,
    current_user: User,
):
    """
    Retrieve all items in the authenticated user's cart.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of cart items. Returns an empty list if the user has no cart.
    """
    cart = get_cart_by_customer(
        db,
        current_user.id,
    )

    if cart is None:
        return []

    logger.info(
        "Fetching cart for user %d",
        current_user.id,
    )

    return get_cart_items(
        db,
        cart.id,
    )


def remove_item_from_cart(
    db: Session,
    current_user: User,
    menu_item_id: int,
):
    """
    Remove a menu item from the authenticated user's cart.

    Args:
        db: Database session.
        current_user: Authenticated user.
        menu_item_id: ID of the menu item to remove.

    Returns:
        None.
    """
    cart = get_cart_by_customer(
        db,
        current_user.id,
    )

    if cart is None:
        return

    cart_item = get_cart_item(
        db,
        cart.id,
        menu_item_id,
    )

    if cart_item is None:
        return

    logger.info(
        "Removing menu item %d from cart",
        menu_item_id,
    )

    delete_cart_item(
        db,
        cart_item,
    )


def clear_user_cart(
    db: Session,
    current_user: User,
):
    """
    Remove all items from the authenticated user's cart.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        None.
    """
    cart = get_cart_by_customer(
        db,
        current_user.id,
    )

    if cart is None:
        return

    logger.info(
        "Clearing cart for user %d",
        current_user.id,
    )

    clear_cart(
        db,
        cart.id,
    )


def update_cart_item_quantity(
    db: Session,
    current_user: User,
    menu_item_id: int,
    quantity: int,
):
    """
    Update the quantity of a menu item in the authenticated user's cart.

    Args:
        db: Database session.
        current_user: Authenticated user.
        menu_item_id: ID of the menu item.
        quantity: New quantity.

    Returns:
        The updated cart item, or None if the cart does not exist.

    Raises:
        MenuItemNotFoundException: If the menu item is not present in the cart.
    """
    cart = get_cart_by_customer(
        db,
        current_user.id,
    )

    if cart is None:
        logger.warning(
            "Cart not found for user %d",
            current_user.id,
        )
        return None

    cart_item = get_cart_item(
        db,
        cart.id,
        menu_item_id,
    )

    if cart_item is None:
        logger.warning(
            "Menu item %d not found in cart.",
            menu_item_id,
        )
        raise MenuItemNotFoundException()

    cart_item.quantity = quantity

    logger.info(
        "Updated quantity of menu item %d to %d",
        menu_item_id,
        quantity,
    )

    return save_cart_item(
        db,
        cart_item,
    )