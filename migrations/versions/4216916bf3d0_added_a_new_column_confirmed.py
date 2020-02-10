"""added a new column 'confirmed'

Revision ID: 4216916bf3d0
Revises: c1f64326ab4c
Create Date: 2019-12-23 04:12:07.730985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4216916bf3d0'
down_revision = 'c1f64326ab4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
