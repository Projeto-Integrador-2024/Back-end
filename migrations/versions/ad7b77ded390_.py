"""empty message

Revision ID: ad7b77ded390
Revises: e001a1384fd5
Create Date: 2024-11-01 19:30:34.692304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad7b77ded390'
down_revision = 'e001a1384fd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
