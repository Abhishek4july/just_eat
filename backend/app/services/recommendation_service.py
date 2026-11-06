from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.user import User
from app.repositories.recommendation_repository import (
    get_popular_restaurants,
    get_restaurant_by_id,
    get_restaurants_by_cuisine,
    get_user_favorite_restaurant,
    get_user_preference,
)


def get_recommendations(
    db: Session,
    current_user: User,
):
    logger.info(
        "Fetching recommendations for user %d.",
        current_user.id,
    )

    # Step 1: Recommend based on user's preferred cuisine
    preference = get_user_preference(
        db,
        current_user.id,
    )

    if (
        preference
        and preference.favorite_cuisine
    ):
        logger.info(
            "Using cuisine preference '%s' for recommendations.",
            preference.favorite_cuisine,
        )

        restaurants = get_restaurants_by_cuisine(
            db,
            preference.favorite_cuisine,
        )

        if restaurants:
            return restaurants

    # Step 2: Recommend based on order history
    logger.info(
        "No cuisine preference found. Checking order history."
    )

    favorite_restaurant = get_user_favorite_restaurant(
        db,
        current_user.id,
    )

    if favorite_restaurant:
        logger.info(
            "Using customer's order history."
        )

        restaurant_id, _ = favorite_restaurant

        restaurant = get_restaurant_by_id(
            db,
            restaurant_id,
        )

        if restaurant:
            return [restaurant]

    # Step 3: Recommend globally popular restaurants
    logger.info(
        "No order history found. Returning popular restaurants."
    )

    return get_popular_restaurants(
        db,
    )