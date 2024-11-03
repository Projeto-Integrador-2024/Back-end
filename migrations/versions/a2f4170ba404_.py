"""empty message

Revision ID: a2f4170ba404
Revises: 
Create Date: 2024-11-02 22:14:13.319231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2f4170ba404'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ADMS',
    sa.Column('adm_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('cpf', sa.Text(length=11), nullable=False),
    sa.Column('username', sa.Text(length=20), nullable=False),
    sa.Column('senha', sa.Text(length=80), nullable=False),
    sa.PrimaryKeyConstraint('adm_id')
    )
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
    op.create_table('associations',
    sa.Column('aluno_ra', sa.Text(), nullable=False),
    sa.Column('vaga_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['aluno_ra'], ['alunos.ra'], ),
    sa.ForeignKeyConstraint(['vaga_id'], ['vagas.id'], ),
    sa.PrimaryKeyConstraint('aluno_ra', 'vaga_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('associations')
    op.drop_table('vagas')
    op.drop_table('professores')
    op.drop_table('alunos')
    op.drop_table('ADMS')
    # ### end Alembic commands ###