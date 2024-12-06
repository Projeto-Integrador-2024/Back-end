import re
from extensions import db
from flask_login import UserMixin
# from bcrypt import Bcrypt

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class ADM(db.Model, UserMixin):
    __tablename__ = "ADMS"
    adm_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    cpf = db.Column(db.Text(11), nullable=False)

    username = db.Column(db.Text(20), nullable=False)
    senha = db.Column(db.Text(80), nullable=False)

    def __init__(self, nome, cpf, username, senha):
        if not self.valida_cpf(cpf):
            raise InvalidDataError("CPF INVÁLIDO, CPF DEVE TER 11 CARACTERES")
        self.nome = nome
        self.cpf = cpf
        self.username = username
        self.senha = senha

    def get_id(self):
        return self.adm_id

    @staticmethod
    def valida_cpf(cpf):
        return bool(re.match(r'^\d{11}$', cpf))
    
    def __repr__(self):
        return f"Admin(id={self.adm_id}, nome={self.nome}, cpf={self.cpf})"