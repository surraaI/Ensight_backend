"""updating corporates table

Revision ID: e008554b1f5a
Revises: f6e25e011a15
Create Date: 2025-07-23 16:54:53.026752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e008554b1f5a'
down_revision: Union[str, None] = 'f6e25e011a15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'written_by',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'written_by',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
