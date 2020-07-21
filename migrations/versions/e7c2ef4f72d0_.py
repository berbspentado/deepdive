"""empty message

Revision ID: e7c2ef4f72d0
Revises: 2ccaa56c94d4
Create Date: 2020-07-12 20:28:03.491127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7c2ef4f72d0'
down_revision = '2ccaa56c94d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rse_reports', sa.Column('time', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rse_reports', 'time')
    # ### end Alembic commands ###
