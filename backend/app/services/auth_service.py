from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_email
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.core.logger import logger
from app.core.exceptions import InvalidCredentialsException


def login(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    logger.info("Logger is working")

    if not user:
        raise InvalidCredentialsException()

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
            "user_id": user.id,
        }
    )

    return token


from app.repositories.user_repository import get_user_by_email
from app.utils.security import hash_password
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def register_user(db: Session, user_data):
    existing_user = get_user_by_email(
        db=db,
        email=user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user