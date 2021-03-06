"""added method 'gravatar_hash' and column avatar_hash to user model to avoid code duplication and reduce computing power

Revision ID: 097ca5609a4d
Revises: d7055beaffbf
Create Date: 2020-01-13 17:00:55.939507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '097ca5609a4d'
down_revision = 'd7055beaffbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###
