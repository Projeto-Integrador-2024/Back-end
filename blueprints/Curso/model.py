from extensions import db

class Curso(db.Model):
    __tablename__="cursos"
    codigo          = db.Column(db.Text, primary_key=True)
    nome            = db.Column(db.Text, nullable=False)
    #Curso pode ter vários alunos
    alunos = db.relationship('Aluno', backref='curso_do_aluno', lazy=True)

    def __init__(self, codigo, nome, alunos=None):
        self.codigo = codigo
        self.nome = nome
        self.alunos = alunos if alunos is not None else []