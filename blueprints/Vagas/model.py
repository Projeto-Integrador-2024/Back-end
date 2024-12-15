from extensions import db

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

class Vaga(db.Model):
    __tablename__="vagas"
    id              =   db.Column(db.Integer, primary_key=True)
    nome            =   db.Column(db.Text, nullable=False)
    descricao       =   db.Column(db.Text, nullable=False)
    bolsa           =   db.Column(db.Integer,nullable=False)#0=sem bolsa, 1=tem bolsa
    bolsa_valor     =   db.Column(db.Integer,nullable=True)#valor da bolsa
    tipo            =   db.Column(db.Integer, nullable=False)#0=Pesquisa, 1=Extensão
    criador_id      =   db.Column(db.Text, db.ForeignKey('professores.SIAPE'))

    def __repr__(self):
        return f'Vaga:{self.nome}'

    def __init__(self, nome, descricao, bolsa, bolsa_valor, tipo, criador_id):
        self.nome = nome
        self.descricao = descricao
        self.bolsa = bolsa
        self.bolsa_valor = bolsa_valor
        self.tipo = tipo
        self.criador_id = str(criador_id).zfill(7)

    def check_bolsa(self):
        if self.bolsa==0:
            return 'Não possui bolsa'
        else:
            return 'Possui bolsa'
    
    def valor_bolsa(self):
        if self.bolsa==0:
            return 0
        else:
            return self.bolsa_valor
    
    def check_tipo(self):
        if self.tipo==0:
            return 'Pesquisa'
        else:
            return 'Extensão'