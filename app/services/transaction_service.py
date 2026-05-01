from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.models.transaction import (
    PaymentMethod,
    Transaction,
    TransactionStatus,
    TransactionType,
)
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def create_transaction(session: Session, user: User, data: TransactionCreate) -> Transaction:
    from app.services.category_service import match_category  # noqa: PLC0415

    fields = data.model_dump()
    if fields["category_id"] is None:
        fields["category_id"] = match_category(session, user, data.description)

    transaction = Transaction(**fields, user_id=user.id)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def get_transaction(session: Session, user: User, transaction_id: int) -> Transaction | None:
    return (
        session.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id, Transaction.user_id == user.id)
        .first()
    )


def list_transactions(
    session: Session,
    user: User,
    month: int | None = None,
    year: int | None = None,
    transaction_type: TransactionType | None = None,
    transaction_status: TransactionStatus | None = None,
    payment_method: PaymentMethod | None = None,
    category_id: int | None = None,
) -> list[Transaction]:
    query = session.query(Transaction).filter(Transaction.user_id == user.id)

    if month is not None:
        query = query.filter(extract("month", Transaction.transaction_date) == month)
    if year is not None:
        query = query.filter(extract("year", Transaction.transaction_date) == year)
    if transaction_type is not None:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if transaction_status is not None:
        query = query.filter(Transaction.status == transaction_status)
    if payment_method is not None:
        query = query.filter(Transaction.payment_method == payment_method)
    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)

    return query.order_by(Transaction.transaction_date.desc()).all()


def update_transaction(session: Session, transaction: Transaction, data: TransactionUpdate) -> Transaction:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)
    session.commit()
    session.refresh(transaction)
    return transaction


def delete_transaction(session: Session, transaction: Transaction) -> None:
    session.delete(transaction)
    session.commit()
