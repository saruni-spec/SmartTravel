"""booking

Revision ID: 63ad1c55bab3
Revises: 80b3d73d3a36
Create Date: 2023-06-06 20:50:05.712347

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '63ad1c55bab3'
down_revision = '80b3d73d3a36'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the 'route' table
    

    # Drop the foreign key constraint and column from the 'stage' table
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.drop_constraint('stage_ibfk_1', type_='foreignkey')
        batch_op.drop_column('route_id')

    op.drop_table('route')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('route_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('stage_ibfk_1', 'route', ['route_id'], ['route_id'])

    op.create_table('route',
    sa.Column('route_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('route_start', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('route_end', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('route_distance', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('route_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
