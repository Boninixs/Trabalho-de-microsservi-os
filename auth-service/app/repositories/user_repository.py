from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.scalar(statement)


def get_user_by_id(session: Session, user_id: UUID) -> User | None:
    return session.get(User, user_id)


def add_user(session: Session, user: User) -> User:
    session.add(user)
    return user
