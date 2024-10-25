import re
from extensions import db

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class Professor(db.Model):
    __tablename__="professores"
    ra              = db.Column(db.Text(8), primary_key=True)#p0000001
    nome            = db.Column(db.Text, nullable=False)
    cpf             = db.Column(db.Text(11), nullable=False)

    def __init__(self, nome, cpf):
        if not self.valida_cpf(cpf):
            raise InvalidDataError("CPF INVÁLIDO, CPF DEVE TER 11 CARACTERES")
        self.ra = self.gera_ra_automatico()
        self.nome = nome
        self.cpf = cpf

    @staticmethod
    def valida_cpf(cpf):
        return bool(re.match(r'^\d{11}$', cpf))

    @staticmethod
    def gera_ra_automatico():
        ultimo_prof = Professor.query.order_by(Professor.ra.desc()).first()
        if ultimo_prof:
            ultimo_numero = int(ultimo_prof.ra[1:])
            novo_numero = ultimo_numero + 1
            return f'p{novo_numero:07d}'
        else:
            return 'p0000001'