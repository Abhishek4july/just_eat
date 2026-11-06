import app.main

from sqlalchemy.orm import configure_mappers
from app.db.database import Base
from app.models.user import User

from app.db.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password
from sqlalchemy.orm import Session

def seed_users(db: Session):
    print("Inside seed_users")

    customer = db.query(User).filter(
        User.email == "customer@test.com"
    ).first()

    print("Customer:", customer)

    if not customer:
        print("Creating customer")
        customer = User(
            username="customer",
            email="customer@test.com",
            hashed_password=hash_password("customer123"),
            role="CUSTOMER",
        )
        db.add(customer)

    owner = db.query(User).filter(
        User.email == "owner@test.com"
    ).first()

    print("Owner:", owner)

    if not owner:
        print("Creating owner")
        owner = User(
            username="owner",
            email="owner@test.com",
            hashed_password=hash_password("owner123"),
            role="RESTAURANT_OWNER",
        )
        db.add(owner)

    print("Committing...")
    db.commit()
    print("Committed")

def main():
    print("Starting seed")

    db = SessionLocal()
    try:
        seed_users(db)
        print("Users seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()