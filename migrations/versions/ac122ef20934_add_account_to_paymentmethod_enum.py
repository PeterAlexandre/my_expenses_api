"""add_account_to_paymentmethod_enum

Revision ID: ac122ef20934
Revises: f0dccd00a07c
Create Date: 2026-05-02 00:29:11.574259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac122ef20934'
down_revision: Union[str, Sequence[str], None] = 'f0dccd00a07c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE paymentmethod ADD VALUE IF NOT EXISTS 'account'")


def downgrade() -> None:
    # PostgreSQL has no DROP VALUE; recreate the enum without 'account'.
    # Rows with payment_method='account' are nulled out first to avoid cast failure.
    op.execute("UPDATE transactions SET payment_method = NULL WHERE payment_method = 'account'")
    op.execute("ALTER TABLE transactions ALTER COLUMN payment_method TYPE VARCHAR(50)")
    op.execute("DROP TYPE paymentmethod")
    op.execute("CREATE TYPE paymentmethod AS ENUM ('credit_card')")
    op.execute(
        "ALTER TABLE transactions ALTER COLUMN payment_method "
        "TYPE paymentmethod USING payment_method::paymentmethod"
    )
