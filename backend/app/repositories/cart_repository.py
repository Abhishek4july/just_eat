from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


def get_cart_by_customer(
    db: Session,
    customer_id: int,
):
    """
    Retrieve the cart belonging to a specific customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        The customer's cart if it exists, otherwise None.
    """
    return (
        db.query(Cart)
        .filter(Cart.customer_id == customer_id)
        .first()
    )


def create_cart(
    db: Session,
    customer_id: int,
):
    """
    Create a new cart for a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        The newly created cart.
    """
    cart = Cart(
        customer_id=customer_id,
    )

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def get_cart_item(
    db: Session,
    cart_id: int,
    menu_item_id: int,
):
    """
    Retrieve a specific cart item from a cart.

    Args:
        db: Database session.
        cart_id: ID of the cart.
        menu_item_id: ID of the menu item.

    Returns:
        The matching cart item if found, otherwise None.
    """
    return (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.menu_item_id == menu_item_id,
        )
        .first()
    )


def create_cart_item(
    db: Session,
    cart_id: int,
    menu_item_id: int,
    quantity: int,
):
    """
    Add a new item to a cart.

    Args:
        db: Database session.
        cart_id: ID of the cart.
        menu_item_id: ID of the menu item.
        quantity: Quantity of the menu item.

    Returns:
        The newly created cart item.
    """
    cart_item = CartItem(
        cart_id=cart_id,
        menu_item_id=menu_item_id,
        quantity=quantity,
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def save_cart_item(
    db: Session,
    cart_item: CartItem,
):
    """
    Save changes made to an existing cart item.

    Args:
        db: Database session.
        cart_item: Cart item to update.

    Returns:
        The updated cart item.
    """
    db.commit()
    db.refresh(cart_item)

    return cart_item


def get_cart_items(
    db: Session,
    cart_id: int,
):
    """
    Retrieve all items in a cart.

    Args:
        db: Database session.
        cart_id: ID of the cart.

    Returns:
        A list of cart items.
    """
    return (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id)
        .all()
    )


def delete_cart_item(
    db: Session,
    cart_item: CartItem,
):
    """
    Remove a specific item from a cart.

    Args:
        db: Database session.
        cart_item: Cart item to delete.

    Returns:
        None.
    """
    db.delete(cart_item)
    db.commit()


def clear_cart(
    db: Session,
    cart_id: int,
):
    """
    Remove all items from a cart.

    Args:
        db: Database session.
        cart_id: ID of the cart.

    Returns:
        None.
    """
    (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id)
        .delete(synchronize_session=False)
    )

    db.commit()