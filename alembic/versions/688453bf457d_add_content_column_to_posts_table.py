"""add content column to posts table

Revision ID: 688453bf457d
Revises: 42b86da62610
Create Date: 2022-02-06 14:06:53.824564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '688453bf457d'
down_revision = '42b86da62610'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
