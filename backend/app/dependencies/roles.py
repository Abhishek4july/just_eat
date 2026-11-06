from fastapi import Depends
from app.core.exceptions import UnauthorizedException
from app.dependencies.auth import get_current_user
from app.models.user import User


def require_customer(
        current_user:User=Depends(get_current_user),
):
    if current_user.role!="CUSTOMER":
        raise UnauthorizedException()
    return current_user

def require_restaurant_owner(
        current_user:User=Depends(get_current_user),
):
    if current_user.role!="RESTAURANT_OWNER":
        raise UnauthorizedException()
    return current_user