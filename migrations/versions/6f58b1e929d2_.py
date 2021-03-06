"""empty message

Revision ID: 6f58b1e929d2
Revises: e9e8d7aa0d83
Create Date: 2022-03-03 20:10:29.921418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f58b1e929d2'
down_revision = 'e9e8d7aa0d83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category2', sa.Column('c1id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'category2', 'category1', ['c1id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category2', type_='foreignkey')
    op.drop_column('category2', 'c1id')
    # ### end Alembic commands ###
