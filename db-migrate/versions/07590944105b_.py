"""empty message

Revision ID: 07590944105b
Revises: ea22711dcc0a
Create Date: 2022-12-26 20:57:19.184510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07590944105b'
down_revision = 'ea22711dcc0a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    op.drop_column('posts', 'content')
    # ### end Alembic commands ###