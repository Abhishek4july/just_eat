from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str,
):
    """
    Retrieve a user by their email address.

    Args:
        db: Database session.
        email: User's email address.

    Returns:
        The user if found, otherwise None.
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int,
):
    """
    Retrieve a user by their ID.

    Args:
        db: Database session.
        user_id: ID of the user.

    Returns:
        The user if found, otherwise None.
    """
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def save_user(
    db: Session,
    user: User,
):
    """
    Save changes made to a user.

    Args:
        db: Database session.
        user: User object to update.

    Returns:
        The updated user.
    """
    db.commit()
    db.refresh(user)

    return user