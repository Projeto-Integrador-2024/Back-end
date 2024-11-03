"""empty message

Revision ID: f8f8ee1238f7
Revises: 270c92180808
Create Date: 2024-10-25 23:36:53.539002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8f8ee1238f7'
down_revision = '270c92180808'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alunos',
    sa.Column('ra', sa.Text(length=8), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('periodo', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.Text(length=11), nullable=False),
    sa.PrimaryKeyConstraint('ra')
    )
    op.create_table('professores',
    sa.Column('ra', sa.Text(length=8), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('cpf', sa.Text(length=11), nullable=False),
    sa.PrimaryKeyConstraint('ra')
    )
    op.create_table('vagas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('bolsa', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.Integer(), nullable=False),
    sa.Column('criador_id', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['criador_id'], ['professores.ra'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vagas')
    op.drop_table('professores')
    op.drop_table('alunos')
    # ### end Alembic commands ###
