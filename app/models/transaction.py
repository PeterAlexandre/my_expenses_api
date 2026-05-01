from datetime import date
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.transaction_category import TransactionCategory
    from app.models.user import User


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionStatus(str, Enum):
    done = "done"
    provision = "provision"


class PaymentMethod(str, Enum):
    credit_card = "credit_card"
    account = "account"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType), nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        SAEnum(TransactionStatus), nullable=False, default=TransactionStatus.done
    )
    payment_method: Mapped[PaymentMethod | None] = mapped_column(
        SAEnum(PaymentMethod), nullable=True
    )
    is_recurring: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Only for credit_card expenses
    creditcard: Mapped[str | None] = mapped_column(String(4), nullable=True)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("transaction_categories.category_id"),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["TransactionCategory"] = relationship(
        "TransactionCategory",
        back_populates="transactions",
    )
