from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class Period(BaseModel):
    year: int
    month: int


class Summary(BaseModel):
    income_total: Decimal
    expenses_total: Decimal
    difference: Decimal


class CategorySummary(BaseModel):
    category_id: int | None
    name: str
    total: Decimal
    percentage: float


class ProvisionTransaction(BaseModel):
    transaction_id: int
    description: str
    amount: Decimal
    transaction_date: date


class ProvisionsSection(BaseModel):
    total: Decimal
    transactions: list[ProvisionTransaction]


class ProvisionsBlock(BaseModel):
    to_receive: ProvisionsSection
    to_pay: ProvisionsSection


class MonthlyReport(BaseModel):
    period: Period
    summary: Summary
    credit_card_total: Decimal
    current_balance: Decimal
    by_category: list[CategorySummary]
    provisions: ProvisionsBlock
