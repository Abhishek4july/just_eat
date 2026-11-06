from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_id,
    save_user,
)
from app.utils.security import (
    hash_password,
    verify_password,
)
from app.core.exceptions import InvalidCredentialsException

def update_profile(
    db: Session,
    current_user: User,
    username: str,
):
    logger.info(
        "Updating profile for user %d.",
        current_user.id,
    )

    user = get_user_by_id(
        db,
        current_user.id,
    )

    user.username = username

    logger.info(
        "Username updated for user %d.",
        current_user.id,
    )

    return save_user(
        db,
        user,
    )


def change_password(
    db: Session,
    current_user: User,
    current_password: str,
    new_password: str,
):
    logger.info(
        "Changing password for user %d.",
        current_user.id,
    )

    user = get_user_by_id(
        db,
        current_user.id,
    )

    if not verify_password(
        current_password,
        user.hashed_password,
    ):
        logger.warning(
            "Invalid current password for user %d.",
            current_user.id,
        )

        raise InvalidCredentialsException()

    user.hashed_password = hash_password(
        new_password,
    )

    logger.info(
        "Password changed successfully for user %d.",
        current_user.id,
    )

    return save_user(
        db,
        user,
    )