import re
from extensions import db
from flask import jsonify
from flask_login import UserMixin


class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class Professor(db.Model, UserMixin):
    __tablename__="professores"
    ra              = db.Column(db.Text(8), primary_key=True)#p0000001
    nome            = db.Column(db.Text, nullable=False)
    cpf             = db.Column(db.Text(11), nullable=False)
    vagas_criadas   = db.relationship('Vaga',backref='criador')
    senha           = db.Column(db.Text(80), nullable=False)

    def __init__(self, nome, cpf, senha):
        if not self.valida_cpf(cpf):
            raise InvalidDataError("CPF INVÁLIDO, CPF DEVE TER 11 CARACTERES")
        self.ra = self.gera_ra_automatico()
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
    
    def criar_vaga(self, nome, descricao, bolsa, tipo):
        from blueprints.Vagas.model import Vaga
        nova_vaga = Vaga(
            nome=nome,
            descricao=descricao,
            bolsa=bolsa,
            tipo=tipo,
            criador_id=self.ra
        )
        self.vagas_criadas.append(nova_vaga)
        db.session.add(nova_vaga)
        db.session.commit()
        return "vaga criada"
    
    def deletar_vaga(self,id_vaga):
        from blueprints.Vagas.model import Vaga
        vaga = Vaga.query.get(id_vaga)
        if vaga and vaga.criador_id == self.ra:
            db.session.delete(vaga)
            db.session.commit()
            return "vaga deletada"

    def get_id(self):
        return self.ra
    
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