from collections import defaultdict
from decimal import Decimal

from sqlalchemy import extract
from sqlalchemy.orm import Session, joinedload

from app.models.transaction import PaymentMethod, Transaction, TransactionStatus, TransactionType
from app.models.user import User
from app.schemas.report import (
    CategorySummary,
    MonthlyReport,
    Period,
    ProvisionTransaction,
    ProvisionsBlock,
    ProvisionsSection,
    Summary,
)

ZERO = Decimal(0)


def get_monthly_report(session: Session, user: User, year: int, month: int) -> MonthlyReport:
    transactions = (
        session.query(Transaction)
        .options(joinedload(Transaction.category))
        .filter(
            Transaction.user_id == user.id,
            extract("year", Transaction.transaction_date) == year,
            extract("month", Transaction.transaction_date) == month,
        )
        .all()
    )

    income = [t for t in transactions if t.transaction_type == TransactionType.income]
    expenses = [t for t in transactions if t.transaction_type == TransactionType.expense]

    income_total = sum((t.amount for t in income), ZERO)
    expenses_total = sum((t.amount for t in expenses), ZERO)

    credit_card_total = sum(
        (t.amount for t in expenses if t.payment_method == PaymentMethod.credit_card),
        ZERO,
    )

    current_balance = _calculate_balance(session, user)

    by_category = _build_category_breakdown(expenses, expenses_total)

    provision_income = [t for t in income if t.status == TransactionStatus.provision]
    provision_expenses = [t for t in expenses if t.status == TransactionStatus.provision]

    provisions = ProvisionsBlock(
        to_receive=ProvisionsSection(
            total=sum((t.amount for t in provision_income), ZERO),
            transactions=_to_lightweight(provision_income),
        ),
        to_pay=ProvisionsSection(
            total=sum((t.amount for t in provision_expenses), ZERO),
            transactions=_to_lightweight(provision_expenses),
        ),
    )

    return MonthlyReport(
        period=Period(year=year, month=month),
        summary=Summary(
            income_total=income_total,
            expenses_total=expenses_total,
            difference=income_total - expenses_total,
        ),
        credit_card_total=credit_card_total,
        current_balance=current_balance,
        by_category=by_category,
        provisions=provisions,
    )


def _calculate_balance(session: Session, user: User) -> Decimal:
    query = (
        session.query(Transaction)
        .filter(
            Transaction.user_id == user.id,
            Transaction.status == TransactionStatus.done,
        )
    )

    if user.balance_snapshot_date is not None:
        query = query.filter(Transaction.transaction_date > user.balance_snapshot_date)

    all_done = query.all()

    income_total = sum(
        (t.amount for t in all_done if t.transaction_type == TransactionType.income),
        ZERO,
    )
    account_expenses_total = sum(
        (t.amount for t in all_done
         if t.transaction_type == TransactionType.expense
         and t.payment_method == PaymentMethod.account),
        ZERO,
    )

    snapshot = user.balance_snapshot_amount or ZERO
    return snapshot + income_total - account_expenses_total


def _build_category_breakdown(
    expenses: list[Transaction],
    expenses_total: Decimal,
) -> list[CategorySummary]:
    totals: dict[str, Decimal] = defaultdict(lambda: ZERO)

    for transaction in expenses:
        name = transaction.category.name if transaction.category else "Uncategorized"
        totals[name] += transaction.amount

    return [
        CategorySummary(
            name=name,
            total=total,
            percentage=round(float(total / expenses_total * 100), 2) if expenses_total else 0.0,
        )
        for name, total in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]


def _to_lightweight(transactions: list[Transaction]) -> list[ProvisionTransaction]:
    return [
        ProvisionTransaction(
            transaction_id=transaction.transaction_id,
            description=transaction.description,
            amount=transaction.amount,
            transaction_date=transaction.transaction_date,
        )
        for transaction in transactions
    ]
