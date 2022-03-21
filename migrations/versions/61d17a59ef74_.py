"""empty message

Revision ID: 61d17a59ef74
Revises: 5c5f87daea0d
Create Date: 2022-03-03 20:20:24.857577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d17a59ef74'
down_revision = '5c5f87daea0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('content_ibfk_4', 'content', type_='foreignkey')
    op.create_foreign_key(None, 'content', 'category1', ['c1id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'content', type_='foreignkey')
    op.create_foreign_key('content_ibfk_4', 'content', 'category2', ['c1id'], ['c1id'])
    # ### end Alembic commands ###
