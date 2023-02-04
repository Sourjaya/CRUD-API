"""added users table

Revision ID: 1c97925060a9
Revises: 1736bc029d06
Create Date: 2023-02-04 19:58:59.280998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c97925060a9'
down_revision = '1736bc029d06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False,index=True),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
