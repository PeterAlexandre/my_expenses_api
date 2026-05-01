from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.security import get_current_user
from app.services.user_service import (
    create_user,
    delete_user,
    get_user_by_email,
    update_user,
)

router = APIRouter(prefix="/account", tags=["account"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(data: UserCreate, session: Session = Depends(get_session)):
    existing = get_user_by_email(session, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )
    return create_user(session, data)


@router.get("", response_model=UserRead)
def detail(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("", response_model=UserRead)
def update(
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_user(session, current_user, data)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    delete_user(session, current_user)
