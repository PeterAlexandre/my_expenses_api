from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.transaction_category import TransactionCategory


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    balance_snapshot_amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    balance_snapshot_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="user",
    )
    categories: Mapped[list["TransactionCategory"]] = relationship(
        "TransactionCategory",
        back_populates="user",
    )
