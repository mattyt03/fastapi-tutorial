"""create posts table

Revision ID: 42b86da62610
Revises: 
Create Date: 2022-02-06 04:07:14.077071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42b86da62610'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')