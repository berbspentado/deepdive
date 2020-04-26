"""empty message

Revision ID: 762c2011e5dc
Revises: fbaedff1ebe9
Create Date: 2020-04-19 20:07:58.847160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '762c2011e5dc'
down_revision = 'fbaedff1ebe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('manual_analysis', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('manual_analysis', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('manual_analysis', 'updated_at')
    op.drop_column('manual_analysis', 'created_at')
    # ### end Alembic commands ###