"""empty message

Revision ID: c3bc44994dd7
Revises: ffa7f762746f
Create Date: 2023-04-30 22:54:11.112102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3bc44994dd7'
down_revision = 'ffa7f762746f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.alter_column('original',
               existing_type=sa.TEXT(),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.alter_column('original',
               existing_type=sa.String(length=256),
               type_=sa.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
