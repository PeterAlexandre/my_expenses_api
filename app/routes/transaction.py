from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.models.transaction import PaymentMethod, Transaction, TransactionStatus, TransactionType
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.security import get_current_user
from app.services.transaction_service import (
    create_transaction,
    delete_transaction,
    get_transaction,
    list_transactions,
    update_transaction,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transaction_or_404(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Transaction:
    transaction = get_transaction(session, current_user, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return transaction


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create(
    data: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_transaction(session, current_user, data)


@router.get("", response_model=list[TransactionRead])
def list_all(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = Query(default=None, ge=2000),
    transaction_type: TransactionType | None = Query(default=None, alias="type"),
    transaction_status: TransactionStatus | None = Query(default=None, alias="status"),
    payment_method: PaymentMethod | None = Query(default=None),
    category_id: int | None = Query(default=None),
):
    return list_transactions(
        session,
        current_user,
        month=month,
        year=year,
        transaction_type=transaction_type,
        transaction_status=transaction_status,
        payment_method=payment_method,
        category_id=category_id,
    )


@router.get("/{transaction_id}", response_model=TransactionRead)
def detail(transaction: Transaction = Depends(get_transaction_or_404)):
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
def update(
    data: TransactionUpdate,
    session: Session = Depends(get_session),
    transaction: Transaction = Depends(get_transaction_or_404),
):
    return update_transaction(session, transaction, data)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    session: Session = Depends(get_session),
    transaction: Transaction = Depends(get_transaction_or_404),
):
    delete_transaction(session, transaction)
