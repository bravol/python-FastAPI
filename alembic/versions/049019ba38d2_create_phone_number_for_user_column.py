"""Create phone number for user column

Revision ID: 049019ba38d2
Revises: 
Create Date: 2024-10-17 12:44:13.800197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '049019ba38d2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))



def downgrade() -> None:
    op.drop_column('users','phone_number')
