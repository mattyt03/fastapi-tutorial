"""add remaining columns to posts table

Revision ID: 6923a803f158
Revises: e7228242ae6a
Create Date: 2022-02-06 16:11:04.967561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6923a803f158'
down_revision = 'e7228242ae6a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, 
                                    server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                    server_default=sa.text('now()'), nullable=False))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
