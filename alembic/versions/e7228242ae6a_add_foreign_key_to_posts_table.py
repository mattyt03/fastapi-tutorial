"""add foreign key to posts table

Revision ID: e7228242ae6a
Revises: 938e9e0ab5f0
Create Date: 2022-02-06 14:54:35.950902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7228242ae6a'
down_revision = '938e9e0ab5f0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), 
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))


def downgrade():
    op.drop_column('posts', 'owner_id')