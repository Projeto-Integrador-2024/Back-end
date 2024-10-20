"""empty message

Revision ID: e3a7d837c27a
Revises: 9ce8bc79e274
Create Date: 2024-10-20 19:59:02.927719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3a7d837c27a'
down_revision = '9ce8bc79e274'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alunos',
    sa.Column('ra', sa.Text(length=8), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('periodo', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ra')
    )
    op.create_table('cursos',
    sa.Column('codigo', sa.Text(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('codigo')
    )
    op.create_table('professores',
    sa.Column('ra', sa.Text(length=8), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('cpf', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ra')
    )
    op.drop_table('user')
    op.drop_table('aluno')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aluno',
    sa.Column('RA', sa.INTEGER(), nullable=False),
    sa.Column('cpf', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('RA')
    )
    op.create_table('user',
    sa.Column('uid', sa.INTEGER(), nullable=False),
    sa.Column('usuário', sa.TEXT(), nullable=False),
    sa.Column('senha', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.drop_table('professores')
    op.drop_table('cursos')
    op.drop_table('alunos')
    # ### end Alembic commands ###
