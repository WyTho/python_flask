"""add graph_id to event

Revision ID: 9eedfbbf75ab
Revises: 46ef1d69403a
Create Date: 2019-01-21 11:52:33.827545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eedfbbf75ab'
down_revision = '46ef1d69403a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('_event', sa.Column('graph_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('_event', 'graph_id')
