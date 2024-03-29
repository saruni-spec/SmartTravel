"""empty message

Revision ID: 48b08defa06d
Revises: 
Create Date: 2023-07-17 10:48:35.585310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48b08defa06d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.drop_column('rating')
        batch_op.drop_column('balance')

    # ### end Alembic commands ###
