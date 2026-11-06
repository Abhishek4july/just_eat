from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import User
from app.repositories.preference_repository import (
    create_preference,
    get_preference_by_customer,
    save_preference,
)


def get_preferences(
    db: Session,
    current_user: User,
):
    logger.info(
        "Fetching preferences for user %d.",
        current_user.id,
    )

    preference = get_preference_by_customer(
        db,
        current_user.id,
    )

    return preference


def update_preferences(
    db: Session,
    current_user: User,
    favorite_cuisine: str | None,
    dietary_restriction: str | None,
):
    logger.info(
        "Updating preferences for user %d.",
        current_user.id,
    )

    preference = get_preference_by_customer(
        db,
        current_user.id,
    )

    if preference is None:

        logger.info(
            "Creating preferences for user %d.",
            current_user.id,
        )

        return create_preference(
            db,
            current_user.id,
            favorite_cuisine,
            dietary_restriction,
        )

    preference.favorite_cuisine = favorite_cuisine
    preference.dietary_restriction = dietary_restriction

    logger.info(
        "Preferences updated for user %d.",
        current_user.id,
    )

    return save_preference(
        db,
        preference,
    )