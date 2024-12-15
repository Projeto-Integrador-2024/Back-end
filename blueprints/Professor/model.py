from extensions import db
from flask_login import UserMixin

class Professor(db.Model, UserMixin):
    __tablename__="professores"
    SIAPE           = db.Column(db.Text(7), primary_key=True)
    nome            = db.Column(db.Text, nullable=False)
    cpf             = db.Column(db.Text(11), nullable=False)
    senha           = db.Column(db.Text, nullable=False)
    vagas_criadas   = db.relationship('Vaga',backref='criador')

    def __init__(self,SIAPE, nome, cpf, senha):
        self.SIAPE = SIAPE.zfill(7) 
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
    
    def get_id(self):
        return self.SIAPE
 