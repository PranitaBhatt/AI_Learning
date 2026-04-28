"""Create phone number for user column

Revision ID: 57d6a31df839
Revises: 
Create Date: 2026-04-28 11:49:31.410099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57d6a31df839'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String,nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')