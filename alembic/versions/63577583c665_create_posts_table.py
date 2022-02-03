"""Create posts table

Revision ID: 63577583c665
Revises: 
Create Date: 2022-02-03 21:00:26.035919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63577583c665'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('posts')
