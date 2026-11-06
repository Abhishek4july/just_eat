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