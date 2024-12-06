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

class Aluno(db.Model, UserMixin):
    __tablename__ = "alunos"
    ra = db.Column(db.Text(8), primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    periodo = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.Text(11), nullable=False)
    vagas = db.relationship('Vaga', secondary=association_table, backref='candidatos')
    senha = db.Column(db.Text(80), nullable=False)

    def __init__(self, nome, periodo, cpf, senha):
        if not self.valida_cpf(cpf):
            raise InvalidDataError("CPF INVÁLIDO, CPF DEVE TER 11 CARACTERES")
        if not self.valida_periodo(periodo):
            raise InvalidDataError("PERÍODO INVÁLIDO, PERÍODO DEVE SER UM NÚMERO ENTRE 1 E 8")
        self.ra = self.gera_ra_automatico()
        self.nome = nome
        self.periodo = periodo
        self.cpf = cpf
        self.senha = senha

    def increver(self, ra, id_vaga):
        from blueprints.Vagas.model import Vaga
        aluno = Aluno.query.get(ra) 
        vaga = Vaga.query.get(id_vaga) 
        if aluno.ra == self.ra:
            aluno.vagas.append(vaga) 
            db.session.commit()
            return f"Aluno {ra} inscrito na vaga {id_vaga}"
    
    def desinscrever(self, ra, id_vaga):
        from blueprints.Vagas.model import Vaga
        aluno = Aluno.query.get(ra) 
        vaga = Vaga.query.get(id_vaga)
        if aluno.ra == self.ra: 
            aluno.vagas.remove(vaga)
            db.session.commit()
            return f"Aluno {ra} não está mais inscrito na vaga {id_vaga}"
    
    def get_id(self):
        return self.ra

    @staticmethod
    def valida_cpf(cpf):
        return bool(re.match(r'^\d{11}$', cpf))
    
    @staticmethod
    def valida_periodo(periodo):
        return bool(1 <= periodo <= 8)

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