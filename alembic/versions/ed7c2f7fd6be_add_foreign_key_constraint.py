"""add foreign key constraint

Revision ID: ed7c2f7fd6be
Revises: 109f581d5ac5
Create Date: 2023-02-04 20:08:27.326321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed7c2f7fd6be'
down_revision = '109f581d5ac5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
