from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    uid     = db.Column(db.Integer, primary_key=True)
    usuário = db.Column(db.Text, nullable=False)
    senha   = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Usuário: {self.username}'
    def get_id(self):
        return self.uid
