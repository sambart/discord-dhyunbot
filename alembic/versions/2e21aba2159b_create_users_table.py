"""create users table

Revision ID: 2e21aba2159b
Revises: 
Create Date: 2024-05-11 17:01:50.648389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e21aba2159b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():alembic upgrade head
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('fullname', sa.String),
        sa.Column('nickname', sa.String),
    )

def downgrade():
    op.drop_table('users')