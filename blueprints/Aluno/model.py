import re
from extensions import db

class Aluno(db.Model):
    __tablename__ = "alunos"
    ra = db.Column(db.Text(8), primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    nome_do_curso = db.Column(db.Text, db.ForeignKey('cursos.nome'),nullable=False)


    def __init__(self, nome, periodo, cpf, nome_do_curso):
        if not self.valida_cpf(cpf):
            raise ValueError("CPF inválido. Deve ter exatamente 11 números.")
        if not self.valida_periodo(periodo):
            raise ValueError("Período inválido. Deve ser um número entre 1 e 8.")
        if not self.valida_curso(nome_do_curso):
            raise ValueError("Nome do curso inválido. Este curso não existe.")
        self.ra = self.gera_ra_automatico()
        self.nome = nome
        self.periodo = periodo
        self.cpf = cpf
        self.nome_do_curso = nome_do_curso

    @staticmethod
    def valida_curso(nome_do_curso):
        from blueprints.Curso.model import Curso
        return db.session.query(db.exists().where(Curso.nome == nome_do_curso)).scalar()

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