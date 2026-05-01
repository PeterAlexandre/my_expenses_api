from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.user import User


class TransactionCategory(Base):
    __tablename__ = "transaction_categories"
    __table_args__ = (UniqueConstraint("name", "user_id", name="uq_category_name_user"),)

    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    pattern: Mapped[str | None] = mapped_column(String(500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="category",
    )
