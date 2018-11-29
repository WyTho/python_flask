"""updating Usage

Revision ID: 0da94044aecc
Revises: b25d3cdaca76
Create Date: 2018-11-27 15:02:05.797047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0da94044aecc'
down_revision = 'b25d3cdaca76'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('_usage', sa.Column('address', sa.String(255), nullable=False))
    op.add_column('_usage', sa.Column('unit', sa.String(255), nullable=False))
    op.add_column('_usage', sa.Column('min_value', sa.Integer, nullable=False))
    op.add_column('_usage', sa.Column('max_value', sa.Integer, nullable=False))

    op.drop_column('_item', 'address')


def downgrade():
    op.drop_column('_usage', 'address')
    op.drop_column('_usage', 'unit')
    op.drop_column('_usage', 'min_value')
    op.drop_column('_usage', 'max_value')

    op.add_column('_item', sa.Column('address', sa.String(255), nullable=False))
