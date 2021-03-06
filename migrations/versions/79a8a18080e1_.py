"""empty message

Revision ID: 79a8a18080e1
Revises: 321e0eadf7c8
Create Date: 2018-10-17 11:29:35.315925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a8a18080e1'
down_revision = '321e0eadf7c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('usage', sa.Float(), nullable=True))
    op.add_column('item', sa.Column('usage_type', sa.Enum('KILOWATT_HOUR', 'value', name='usagetypeenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'usage_type')
    op.drop_column('item', 'usage')
    # ### end Alembic commands ###
