"""empty message

Revision ID: 16a665530a3c
Revises: a2f4170ba404
Create Date: 2024-11-03 00:07:10.023112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a665530a3c'
down_revision = 'a2f4170ba404'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('alunos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha', sa.Text(length=80), nullable=False))

    with op.batch_alter_table('professores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha', sa.Text(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('professores', schema=None) as batch_op:
        batch_op.drop_column('senha')

    with op.batch_alter_table('alunos', schema=None) as batch_op:
        batch_op.drop_column('senha')

    # ### end Alembic commands ###