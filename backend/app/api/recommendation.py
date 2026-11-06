from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.restaurant import RestaurantResponse
from app.services.recommendation_service import get_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "",
    response_model=List[RestaurantResponse],
)
def recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve personalized restaurant recommendations for the authenticated user.

    Recommendations are generated based on the user's preferences,
    favorite restaurants, and other relevant factors.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        A list of recommended restaurants.
    """
    return get_recommendations(
        db,
        current_user,
    )