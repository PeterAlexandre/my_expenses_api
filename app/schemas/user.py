from datetime import date
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    balance_snapshot_amount: Decimal | None
    balance_snapshot_date: date | None

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    balance_snapshot_amount: Decimal | None = None
    balance_snapshot_date: date | None = None
