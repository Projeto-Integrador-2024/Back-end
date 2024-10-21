import re
from app import db
from flask_login import UserMixin

class Aluno(db.Model):
    __tablename__ = "alunos"
    ra = db.Column(db.Text(8), primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(11), nullable=False)

    def __init__(self, nome, periodo, cpf):
        if not self.valida_cpf(cpf):
            raise ValueError("CPF inválido. Deve ter exatamente 11 números.")
        if not self.valida_periodo(periodo):
            raise ValueError("Período inválido. Deve ser um número entre 1 e 8.")
        self.ra = self.gera_ra_automatico()
        self.nome = nome
        self.periodo = periodo
        self.cpf = cpf

    @staticmethod
    def valida_cpf(cpf):
        return bool(re.match(r'^\d{11}$', cpf))
    
    @staticmethod
    def valida_periodo(periodo):
        return 1 <= periodo <= 8

    @staticmethod
    def gera_ra_automatico():
        ultimo_aluno = Aluno.query.order_by(Aluno.ra.desc()).first()
        if ultimo_aluno:
            ultimo_numero = int(ultimo_aluno.ra[1:])
            novo_numero = ultimo_numero + 1
            return f'a{novo_numero:07d}'
        else:
            return 'a0000001'

    def __repr__(self):
        return f"Aluno(ra={self.ra}, nome={self.nome}, periodo={self.periodo}, cpf={self.cpf})"


class Professor(db.Model):
    __tablename__="professores"
    ra              = db.Column(db.Text(8), primary_key=True)#p1111111
    nome            = db.Column(db.Text, nullable=False)
    cpf             = db.Column(db.Integer, nullable=False)


class Curso(db.Model):
    __tablename__="cursos"
    codigo          = db.Column(db.Text, primary_key=True)
    nome            = db.Column(db.Text, nullable=False)


# class Materia(db.Model):
#     __tablename__="materias"
#     id      = db.Column(db.Integer, primary_key=True)
#     codigo  = db.Column(db.Text, nullable=False)
#     nome    = db.Column(db.Text, nullable=False)
#     dia     = db.Column(db.Text, nullable=False)
#     horario = db.Column(db.Text, nullable=False)

# class Sala(db.Model):
#     __tablename__="salas:"
#     id          = db.Column(db.Integer, primary_key=True)
#     nome        = db.Column(db.Text, nullable=False)
#     capacidade  = db.Column(db.Integer, nullable=False)

