"""add username column to users table

Revision ID: 109f581d5ac5
Revises: 1c97925060a9
Create Date: 2023-02-04 20:06:07.890988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '109f581d5ac5'
down_revision = '1c97925060a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('username',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('users','username')
    pass
