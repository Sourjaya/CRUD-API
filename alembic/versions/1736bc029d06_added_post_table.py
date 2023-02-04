"""added post table

Revision ID: 1736bc029d06
Revises: 
Create Date: 2023-02-04 19:46:59.432863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1736bc029d06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), index=True, nullable=False), sa.Column('title', sa.String(), nullable=False), sa.Column('content', sa.String(), nullable=False), sa.Column('published', sa.Boolean(), nullable=False,server_default='TRUE'), sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), sa.PrimaryKeyConstraint('id'))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
