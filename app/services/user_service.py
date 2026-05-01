from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password


def create_user(session: Session, data: UserCreate) -> User:
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def update_user(session: Session, user: User, data: UserUpdate) -> User:
    if data.name is not None:
        user.name = data.name
    if data.email is not None:
        user.email = data.email
    if data.password is not None:
        user.hashed_password = hash_password(data.password)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
