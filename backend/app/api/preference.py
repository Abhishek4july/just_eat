from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.preference import (
    PreferenceRequest,
    PreferenceResponse,
)
from app.services.preference_service import (
    get_preferences,
    update_preferences,
)

router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


@router.get(
    "",
    response_model=PreferenceResponse | None,
)
def view_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the food preferences of the authenticated user.

    Args:
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The user's preferences if available, otherwise None.
    """
    return get_preferences(
        db,
        current_user,
    )


@router.put(
    "",
    response_model=PreferenceResponse,
)
def edit_preferences(
    preference: PreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create or update the food preferences of the authenticated user.

    Args:
        preference: Updated favorite cuisine and dietary restriction.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        The updated user preferences.
    """
    return update_preferences(
        db=db,
        current_user=current_user,
        favorite_cuisine=preference.favorite_cuisine,
        dietary_restriction=preference.dietary_restriction,
    )