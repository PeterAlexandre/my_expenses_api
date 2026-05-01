from pydantic import BaseModel, EmailStr


class TranscationCreate(BaseModel):
    type: str
    description: str | None = None
    amount: float
    transaction_date: str
    category_id: int
    user_id: int


class TransactionRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class TransactionUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
