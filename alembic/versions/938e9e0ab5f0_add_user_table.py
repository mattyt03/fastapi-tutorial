"""add user table

Revision ID: 938e9e0ab5f0
Revises: 688453bf457d
Create Date: 2022-02-06 14:36:22.990004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938e9e0ab5f0'
down_revision = '688453bf457d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_table('users')
