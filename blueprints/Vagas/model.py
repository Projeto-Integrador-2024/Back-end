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
    tipo            =   db.Column(db.Integer, nullable=False)#0=Pesquisa, 1=Extensão

    criador_id      = db.Column(db.Text, db.ForeignKey('professores.ra'))

    def __repr__(self):
        return f'Vaga:{self.nome}'

    def __init__(self, nome, descricao, bolsa, tipo, criador_id):
        if not self.valida(bolsa,tipo):
            raise InvalidDataError("Valor inválido para bolsa ou tipo")
        self.nome = nome
        self.descricao = descricao
        self.bolsa = bolsa
        self.tipo = tipo
        self.criador_id = criador_id

    @staticmethod
    def valida(bolsa, tipo):
        if bolsa not in (0, 1) or tipo not in (0, 1):
            return False
        else:
            return True

    def check_bolsa(self):
        if self.bolsa==0:
            return 'Não possui bolsa'
        else:
            return 'Possui bolsa'
    
    def check_tipo(self):
        if self.tipo==0:
            return 'Pesquisa'
        else:
            return 'Extensão'