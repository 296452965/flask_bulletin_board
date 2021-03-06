"""empty message

Revision ID: 5c5f87daea0d
Revises: 6f58b1e929d2
Create Date: 2022-03-03 20:16:09.391744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c5f87daea0d'
down_revision = '6f58b1e929d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('c1id', sa.Integer(), nullable=True))
    op.drop_constraint('content_ibfk_1', 'content', type_='foreignkey')
    op.create_foreign_key(None, 'content', 'category2', ['c1id'], ['c1id'])
    op.drop_column('content', 'cid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('cid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'content', type_='foreignkey')
    op.create_foreign_key('content_ibfk_1', 'content', 'category1', ['cid'], ['id'])
    op.drop_column('content', 'c1id')
    # ### end Alembic commands ###
