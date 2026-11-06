from app.schemas.cart import UpdateCartItem
from app.services.cart_service import update_cart_item_quantity
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.cart_service import remove_item_from_cart
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.cart_service import get_user_cart
from app.schemas.cart import (
    AddCartItem,
    CartItemResponse,
)
from app.services.cart_service import (
    add_to_cart,
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_item_to_cart(
    cart_item: AddCartItem,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a menu item to the authenticated user's cart.

    Args:
        cart_item: Menu item ID and quantity to be added.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The newly added or updated cart item.
    """
    return add_to_cart(
        db=db,
        current_user=current_user,
        menu_item_id=cart_item.menu_item_id,
        quantity=cart_item.quantity,
    )


@router.get(
    "",
    response_model=list[CartItemResponse],
)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all items in the authenticated user's cart.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of cart items.
    """
    return get_user_cart(
        db,
        current_user,
    )


@router.put(
    "/items/{menu_item_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    menu_item_id: int,
    cart_item: UpdateCartItem,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the quantity of a specific cart item.

    Args:
        menu_item_id: ID of the menu item.
        cart_item: Updated quantity.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Updated cart item.
    """
    return update_cart_item_quantity(
        db=db,
        current_user=current_user,
        menu_item_id=menu_item_id,
        quantity=cart_item.quantity,
    )


@router.delete(
    "/items/{menu_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_cart_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a menu item from the authenticated user's cart.

    Args:
        menu_item_id: ID of the menu item to remove.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        None.
    """
    remove_item_from_cart(
        db=db,
        current_user=current_user,
        menu_item_id=menu_item_id,
    )