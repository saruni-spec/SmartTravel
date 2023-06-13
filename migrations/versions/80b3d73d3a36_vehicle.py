"""vehicle

Revision ID: 80b3d73d3a36
Revises: de2ca14469af
Create Date: 2023-06-06 12:17:13.078346

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '80b3d73d3a36'
down_revision = 'de2ca14469af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_code', sa.String(length=50), nullable=True))
        batch_op.alter_column('driver_username',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column('driver_username',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('verification_code')

    # ### end Alembic commands ###