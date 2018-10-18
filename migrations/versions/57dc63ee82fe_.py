"""empty message

Revision ID: 57dc63ee82fe
Revises: 11381970b25f
Create Date: 2018-10-04 13:46:19.167196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57dc63ee82fe'
down_revision = '11381970b25f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group')
    # ### end Alembic commands ###
