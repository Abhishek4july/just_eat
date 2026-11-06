from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_restaurant_owner
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from app.services.order_service import (
    create_new_order,
    get_my_orders,
    get_restaurant_order_list,
    update_order_status,
    cancel_order,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new order for the authenticated user.

    Args:
        order: Order details including restaurant and items.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The newly created order.
    """
    return create_new_order(
        db,
        order,
        current_user,
    )


@router.get(
    "/my-orders",
    response_model=list[OrderResponse],
)
def my_orders(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all orders placed by the authenticated user.

    Args:
        search: Optional search keyword for filtering orders.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of the user's orders.
    """
    return get_my_orders(
        db,
        current_user,
        search,
    )


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[OrderResponse],
)
def restaurant_orders(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Retrieve all orders for a specific restaurant.

    Args:
        restaurant_id: ID of the restaurant.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        A list of restaurant orders.
    """
    return get_restaurant_order_list(
        db,
        restaurant_id,
        current_user,
    )


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
)
def update_status(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Update the status of an existing order.

    Args:
        order_id: ID of the order.
        order: Updated order status.
        db: Database session.
        current_user: Authenticated restaurant owner.

    Returns:
        The updated order.
    """
    return update_order_status(
        db,
        order_id,
        order,
        current_user,
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
def cancel_customer_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel an order placed by the authenticated user.

    Args:
        order_id: ID of the order to cancel.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The cancelled order.
    """
    return cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )