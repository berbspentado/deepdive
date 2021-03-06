"""empty message

Revision ID: f7e6a85fc766
Revises: 7f9988f912d8
Create Date: 2020-07-05 16:04:26.721816

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7e6a85fc766'
down_revision = '7f9988f912d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('upload_analysis', 'updated_at')
    op.drop_column('upload_analysis', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload_analysis', sa.Column('created_at', mysql.DATETIME(), nullable=False))
    op.add_column('upload_analysis', sa.Column('updated_at', mysql.DATETIME(), nullable=False))
    # ### end Alembic commands ###
