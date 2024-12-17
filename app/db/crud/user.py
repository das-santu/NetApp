from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.auth import UserCreate


def get_user_by_username_or_email(db: Session, identifier: str) -> User | None:
    """
    Retrieve a user by username or email.
    :param db: SQLAlchemy Session
    :param identifier: Either username or email
    :return: User object or None
    """
    return db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()


def create_user(db: Session, user: UserCreate):
    new_user = User(username=user.username, email=user.email, password=user.password)  # Hash password in production
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
