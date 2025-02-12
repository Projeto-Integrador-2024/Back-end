import re
from extensions import db
from flask_login import UserMixin

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

association_table = db.Table('associations',
    db.Column('aluno_ra', db.Text, db.ForeignKey('alunos.ra'), primary_key=True),
    db.Column('vaga_id', db.Integer, db.ForeignKey('vagas.id'), primary_key=True)
)

favoritos_table = db.Table('favoritadas',
    db.Column('aluno_ra', db.Text, db.ForeignKey('alunos.ra'), primary_key=True),
    db.Column('vaga_id', db.Integer, db.ForeignKey('vagas.id'), primary_key=True)
)

selecionados_table = db.Table('selecionados',
    db.Column('aluno_ra', db.Text, db.ForeignKey('alunos.ra'), primary_key=True),
    db.Column('vaga_id', db.Integer, db.ForeignKey('vagas.id'), primary_key=True)
)

class Aluno(db.Model, UserMixin):
    __tablename__ = "alunos"
    ra = db.Column(db.Text(8), primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.Text(11), nullable=False)
    senha = db.Column(db.Text, nullable=False)

    vagas = db.relationship('Vaga', secondary=association_table, back_populates="candidatos")
    vagas_favoritadas = db.relationship('Vaga', secondary=favoritos_table, back_populates="favoritos")
    vagas_selecionadas = db.relationship('Vaga', secondary=selecionados_table, back_populates="alunos_selecionados")


    def __init__(self ,ra ,nome, periodo, cpf, senha):
        self.ra = ra
        self.nome = nome
        self.periodo = periodo
        self.cpf = cpf
        self.senha = senha
    
    def get_id(self):
        return self.ra

    def __repr__(self):
        return f"Aluno(ra={self.ra}, nome={self.nome}, periodo={self.periodo}, cpf={self.cpf})"