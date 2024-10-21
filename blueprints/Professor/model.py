from extensions import db

class Professor(db.Model):
    __tablename__="professores"
    ra              = db.Column(db.Text(8), primary_key=True)#p1111111
    nome            = db.Column(db.Text, nullable=False)
    cpf             = db.Column(db.Integer, nullable=False)