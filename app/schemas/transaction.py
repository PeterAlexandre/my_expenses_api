from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.transaction import PaymentMethod, TransactionStatus, TransactionType


class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    description: str
    amount: Decimal = Field(gt=0, decimal_places=2)
    transaction_date: date
    status: TransactionStatus = TransactionStatus.done
    payment_method: PaymentMethod | None = None
    is_recurring: bool = False
    creditcard: str | None = Field(default=None, pattern=r"^\d{4}$")
    category_id: int | None = None


class TransactionRead(BaseModel):
    transaction_id: int
    transaction_type: TransactionType
    description: str
    amount: Decimal
    transaction_date: date
    status: TransactionStatus
    payment_method: PaymentMethod | None
    is_recurring: bool
    creditcard: str | None
    category_id: int | None
    user_id: int

    model_config = {"from_attributes": True}


class TransactionUpdate(BaseModel):
    description: str | None = None
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    transaction_date: date | None = None
    status: TransactionStatus | None = None
    payment_method: PaymentMethod | None = None
    is_recurring: bool | None = None
    creditcard: str | None = Field(default=None, pattern=r"^\d{4}$")
    category_id: int | None = None
