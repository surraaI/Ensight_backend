"""Convert enum values to uppercase

Revision ID: cb111da7a44f
Revises: ed848d0d8f92
Create Date: 2025-05-29 01:13:30.903586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cb111da7a44f'
down_revision: Union[str, None] = 'ed848d0d8f92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define old and new enum types
old_enum = postgresql.ENUM(
    'superadmin', 'admin', 'editor', 'writer', 'subscriber', 'free_user',
    name='role'
)
new_enum = postgresql.ENUM(
    'SUPERADMIN', 'ADMIN', 'EDITOR', 'WRITER', 'SUBSCRIBER', 'FREE_USER',
    name='role'
)

def upgrade() -> None:
    # Create a temporary type
    temp_enum = postgresql.ENUM(
        'SUPERADMIN', 'ADMIN', 'EDITOR', 'WRITER', 'SUBSCRIBER', 'FREE_USER',
        name='role_new'
    )
    temp_enum.create(op.get_bind(), checkfirst=False)
    
    # Convert to temporary type
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE role_new 
        USING role::text::role_new
    """)
    
    # Drop old enum
    old_enum.drop(op.get_bind(), checkfirst=False)
    
    # Rename new enum
    op.execute("ALTER TYPE role_new RENAME TO role")
    
    # Convert to final enum
    op.alter_column('users', 'role',
                   type_=new_enum,
                   postgresql_using='role::text::role')

def downgrade() -> None:
    # Create a temporary type
    temp_enum = postgresql.ENUM(
        'superadmin', 'admin', 'editor', 'writer', 'subscriber', 'free_user',
        name='role_old'
    )
    temp_enum.create(op.get_bind(), checkfirst=False)
    
    # Convert to temporary type
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN role TYPE role_old 
        USING LOWER(role::text)::role_old
    """)
    
    # Drop new enum
    new_enum.drop(op.get_bind(), checkfirst=False)
    
    # Rename old enum
    op.execute("ALTER TYPE role_old RENAME TO role")
    
    # Convert to final enum
    op.alter_column('users', 'role',
                   type_=old_enum,
                   postgresql_using='role::text::role')