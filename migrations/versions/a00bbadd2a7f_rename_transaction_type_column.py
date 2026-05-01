"""rename_transaction_type_column

Revision ID: a00bbadd2a7f
Revises: 0713cc4e308e
Create Date: 2026-05-01 17:19:16.876671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a00bbadd2a7f'
down_revision: Union[str, Sequence[str], None] = '0713cc4e308e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('transactions', 'type', new_column_name='transaction_type')


def downgrade() -> None:
    op.alter_column('transactions', 'transaction_type', new_column_name='type')
