"""empty message

Revision ID: 20d1e1ae46ad
Revises: 3518b4bf08c3
Create Date: 2020-01-20 17:50:33.197545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20d1e1ae46ad'
down_revision = '3518b4bf08c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people_quoted', sa.Column('name', sa.String(length=32), nullable=True))
    op.drop_column('people_quoted', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people_quoted', sa.Column('first_name', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_column('people_quoted', 'name')
    # ### end Alembic commands ###