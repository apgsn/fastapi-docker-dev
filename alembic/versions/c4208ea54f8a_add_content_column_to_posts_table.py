"""Add content column to posts table

Revision ID: c4208ea54f8a
Revises: 63577583c665
Create Date: 2022-02-03 21:11:06.438691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4208ea54f8a'
down_revision = '63577583c665'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
