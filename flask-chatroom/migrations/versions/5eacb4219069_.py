"""empty message

Revision ID: 5eacb4219069
Revises: 1145a52ba56e
Create Date: 2019-05-11 15:15:06.290977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eacb4219069'
down_revision = '1145a52ba56e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_url', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_url')
    # ### end Alembic commands ###