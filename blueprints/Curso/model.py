from app import db

class Curso(db.Model):
    __tablename__="cursos"
    codigo          = db.Column(db.Text, primary_key=True)
    nome            = db.Column(db.Text, nullable=False)