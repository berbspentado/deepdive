"""empty message

Revision ID: 15414a8f25e2
Revises: e7c2ef4f72d0
Create Date: 2020-07-12 20:37:40.303834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15414a8f25e2'
down_revision = 'e7c2ef4f72d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rse_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store', sa.String(length=500), nullable=True),
    sa.Column('country', sa.String(length=500), nullable=True),
    sa.Column('lane', sa.String(length=500), nullable=True),
    sa.Column('device', sa.String(length=500), nullable=True),
    sa.Column('rse_date', sa.String(length=500), nullable=True),
    sa.Column('rse_time', sa.String(length=500), nullable=True),
    sa.Column('tender_state', sa.String(length=500), nullable=True),
    sa.Column('state', sa.String(length=500), nullable=True),
    sa.Column('diagfile_name', sa.String(length=500), nullable=True),
    sa.Column('build', sa.String(length=500), nullable=True),
    sa.Column('time', sa.String(length=500), nullable=True),
    sa.Column('analysis', sa.String(length=1000), nullable=True),
    sa.Column('jira', sa.String(length=500), nullable=True),
    sa.Column('Category', sa.String(length=500), nullable=True),
    sa.Column('types_of_reboot', sa.String(length=500), nullable=True),
    sa.Column('gsa_version', sa.String(length=500), nullable=True),
    sa.Column('device_error', sa.String(length=500), nullable=True),
    sa.Column('assign', sa.String(length=500), nullable=True),
    sa.Column('second_review', sa.String(length=500), nullable=True),
    sa.Column('null_data', sa.String(length=500), nullable=True),
    sa.Column('jira_or_gsa', sa.String(length=500), nullable=True),
    sa.Column('operational_review', sa.String(length=500), nullable=True),
    sa.Column('hwtype', sa.String(length=500), nullable=True),
    sa.Column('motherboard', sa.String(length=500), nullable=True),
    sa.Column('operational_reviewed_by', sa.String(length=500), nullable=True),
    sa.Column('sa_server', sa.String(length=500), nullable=True),
    sa.Column('data', sa.String(length=500), nullable=True),
    sa.Column('adk', sa.String(length=500), nullable=True),
    sa.Column('ps_package', sa.String(length=500), nullable=True),
    sa.Column('fix_version', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('upload_analysis_ibfk_1', 'upload_analysis', type_='foreignkey')
    op.drop_column('upload_analysis', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload_analysis', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('upload_analysis_ibfk_1', 'upload_analysis', 'users', ['user_id'], ['id'])
    op.drop_table('rse_reports')
    # ### end Alembic commands ###