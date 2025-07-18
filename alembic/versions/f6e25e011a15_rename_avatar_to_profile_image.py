"""Rename avatar to profile_image

Revision ID: f6e25e011a15
Revises: e45d7fd6eabf
Create Date: 2025-07-15 09:57:34.640647
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'f6e25e011a15'
down_revision: Union[str, None] = 'e45d7fd6eabf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('profiles', sa.Column('profile_image', sa.String(), nullable=True))
    op.drop_column('profiles', 'avatar')

def downgrade() -> None:
    op.add_column('profiles', sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('profiles', 'profile_image')
