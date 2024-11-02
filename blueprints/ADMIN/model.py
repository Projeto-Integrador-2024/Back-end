import re
from extensions import db
from flask import jsonify

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class ADM(db.Model):
    __tablename__ = "ADMS"
    adm_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    cpf = db.Column(db.Text(11), nullable=False)

    def __init__(self, nome, cpf):
        if not self.valida_cpf(cpf):
            raise InvalidDataError("CPF INVÁLIDO, CPF DEVE TER 11 CARACTERES")
        self.nome = nome
        self.cpf = cpf


    @staticmethod
    def valida_cpf(cpf):
        return bool(re.match(r'^\d{11}$', cpf))
    
    def __repr__(self):
        return f"Admin(id={self.adm_id}, nome={self.nome}, cpf={self.cpf})"