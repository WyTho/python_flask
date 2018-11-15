"""empty message

Revision ID: b25d3cdaca76
Revises: 0e7a89dfc312
Create Date: 2018-11-14 14:03:26.825805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b25d3cdaca76'
down_revision = '0e7a89dfc312'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_event_call',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('json', sa.String(25500), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_graph',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(255), nullable=False),
    sa.Column('data_type', sa.Enum('TEMPERATURE', 'WATER_USAGE', 'value', name='datatypeenum'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('address', sa.String(255), nullable=False),
    sa.Column('comment', sa.String(255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_day',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('graph_id', sa.Integer(), nullable=False),
    sa.Column('date_timestamp', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['graph_id'], ['_graph.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_item_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['_group.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('usage_type', sa.Enum('KILOWATT', 'WATER_PER_HOUR', 'WATER_PER_USAGE', 'value', name='usagetypeenum'), nullable=False),
    sa.Column('usage', sa.String(255), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usage_id', sa.Integer(), nullable=True),
    sa.Column('data_type', sa.Enum('TEMPERATURE', 'WATER_USAGE', 'value', name='datatypeenum'), nullable=False),
    sa.Column('data', sa.String(255), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usage_id'], ['_usage.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('_hour',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('hour', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('is_final_value', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['_day.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('event_call')
    op.drop_table('hour')
    op.drop_table('day')
    op.drop_table('event')
    op.drop_table('item_group')
    op.drop_table('graph')
    op.drop_table('usage')
    op.drop_table('item')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('comment', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('usage',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('item_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('usage_type', mysql.ENUM('KILOWATT', 'WATER_PER_HOUR', 'WATER_PER_USAGE', 'value'), nullable=False),
    sa.Column('usage', mysql.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='usage_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('hour',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('day_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('hour', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('value', mysql.FLOAT(), nullable=True),
    sa.Column('is_final_value', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.CheckConstraint('`is_final_value` in (0,1)', name='CONSTRAINT_1'),
    sa.ForeignKeyConstraint(['day_id'], ['day.id'], name='hour_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('graph',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('data_type', mysql.ENUM('TEMPERATURE', 'WATER_USAGE', 'value'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('title', 'graph', ['title'], unique=True)
    op.create_table('item_group',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('item_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('group_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['item.id'], name='item_group_ibfk_1'),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name='item_group_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('event',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('data_type', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('data', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('timestamp', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('usage_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['usage_id'], ['usage.id'], name='event_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('day',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('graph_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('date_timestamp', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['graph_id'], ['graph.id'], name='day_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('event_call',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('json', mysql.VARCHAR(length=2550), nullable=False),
    sa.Column('timestamp', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('_hour')
    op.drop_table('_event')
    op.drop_table('_usage')
    op.drop_table('_item_group')
    op.drop_table('_day')
    op.drop_table('_item')
    op.drop_table('_graph')
    op.drop_table('_event_call')
    # ### end Alembic commands ###
