from sqlalchemy.orm import Session

from app.models.preference import Preference


def get_preference_by_customer(
    db: Session,
    customer_id: int,
):
    """
    Retrieve the preferences of a specific customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.

    Returns:
        The customer's preferences if found, otherwise None.
    """
    return (
        db.query(Preference)
        .filter(
            Preference.customer_id == customer_id,
        )
        .first()
    )


def create_preference(
    db: Session,
    customer_id: int,
    favorite_cuisine: str | None,
    dietary_restriction: str | None,
):
    """
    Create preferences for a customer.

    Args:
        db: Database session.
        customer_id: ID of the customer.
        favorite_cuisine: Customer's favorite cuisine.
        dietary_restriction: Customer's dietary restriction.

    Returns:
        The newly created preference.
    """
    preference = Preference(
        customer_id=customer_id,
        favorite_cuisine=favorite_cuisine,
        dietary_restriction=dietary_restriction,
    )

    db.add(preference)
    db.commit()
    db.refresh(preference)

    return preference


def save_preference(
    db: Session,
    preference: Preference,
):
    """
    Save changes made to an existing preference.

    Args:
        db: Database session.
        preference: Preference object to update.

    Returns:
        The updated preference.
    """
    db.commit()
    db.refresh(preference)

    return preference