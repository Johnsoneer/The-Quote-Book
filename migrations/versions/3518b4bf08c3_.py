"""empty message

Revision ID: 3518b4bf08c3
Revises: 2156b753a963
Create Date: 2020-01-20 17:48:43.323150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3518b4bf08c3'
down_revision = '2156b753a963'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('people_quoted', 'last_name_initial')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people_quoted', sa.Column('last_name_initial', sa.VARCHAR(length=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
