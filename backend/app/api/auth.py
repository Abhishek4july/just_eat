from app.dependencies.roles import require_restaurant_owner
from app.repositories.user_repository import get_user_by_email
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.schemas.user import ChangePassword
from app.services.user_service import change_password
from app.core.logger import logger
from app.core.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session
from app.schemas.user import RegisterUser
from app.services.auth_service import register_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.db.database import get_db
from app.schemas.auth import Token
from app.services.auth_service import login
from app.schemas.user import (
    UpdateProfile,
    UserResponse,
)
from app.services.user_service import update_profile

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and generate a JWT access token.

    Args:
        form_data: Contains the user's email (username field)
                   and password submitted through the login form.
        db: Database session.

    Returns:
        A JWT access token and token type if authentication succeeds.
    """
    token = login(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the profile of the currently authenticated user.

    Args:
        current_user: Authenticated user obtained from JWT.

    Returns:
        Basic information of the logged-in user.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }



@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterUser,
    db: Session = Depends(get_db)
):
    return register_user(
        db=db,
        user_data=user_data
    )




@router.get("/owner-only")
def owner_only(
    current_user: User = Depends(require_restaurant_owner),
):
    """
    Verify that the authenticated user has the Restaurant Owner role.

    Args:
        current_user: Authenticated restaurant owner.

    Returns:
        A welcome message along with the owner's email.
    """
    return {
        "message": "Welcome Owner",
        "email": current_user.email,
    }


@router.put(
    "/me",
    response_model=UserResponse,
)
def update_me(
    profile: UpdateProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the profile details of the authenticated user.

    Args:
        profile: Updated profile information.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Updated user profile.
    """
    return update_profile(
        db=db,
        current_user=current_user,
        username=profile.username,
    )


@router.put(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
def update_password(
    password: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Change the password of the authenticated user.

    Args:
        password: Current and new password details.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        Success message after the password is updated.
    """
    change_password(
        db=db,
        current_user=current_user,
        current_password=password.current_password,
        new_password=password.new_password,
    )

    return {
        "message": "Password changed successfully."
    }