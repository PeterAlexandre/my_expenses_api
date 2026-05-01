from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.models.transaction_category import TransactionCategory
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.security import get_current_user
from app.services.category_service import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_or_404(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TransactionCategory:
    category = get_category(session, current_user, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    return category


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create(
    data: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_category(session, current_user, data)


@router.get("", response_model=list[CategoryRead])
def list_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return list_categories(session, current_user)


@router.get("/{category_id}", response_model=CategoryRead)
def detail(category: TransactionCategory = Depends(get_category_or_404)):
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def update(
    data: CategoryUpdate,
    session: Session = Depends(get_session),
    category: TransactionCategory = Depends(get_category_or_404),
):
    return update_category(session, category, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    session: Session = Depends(get_session),
    category: TransactionCategory = Depends(get_category_or_404),
):
    delete_category(session, category)
