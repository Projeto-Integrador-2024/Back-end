"""empty message

Revision ID: 9ce8bc79e274
Revises: 
Create Date: 2024-10-19 18:58:46.523672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ce8bc79e274'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aluno',
    sa.Column('RA', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.Integer(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('RA')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('usuário', sa.Text(), nullable=False),
    sa.Column('senha', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('aluno')
    # ### end Alembic commands ###
