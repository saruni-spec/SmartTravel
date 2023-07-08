"""empty message

Revision ID: 8b8faf8469ff
Revises: 1124388b9a46
Create Date: 2023-07-05 15:49:54.336560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b8faf8469ff'
down_revision = '1124388b9a46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###   
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('for_hire', sa.Boolean(), default=False))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('build_type', mysql.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('for_hire')

    
