from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionCategory(Base):
    __tablename__ = "transaction_categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pattern: Mapped[str | None] = mapped_column(String(500), nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="category",
    )
