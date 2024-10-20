from flask import request
from flask_login import login_user, logout_user, current_user, login_required
from models import User

def register_routes(app,db,bcrypt):
    @app.route('/')
    def index():
        dados=request.get_json()
        usuário= dados.get('usuário')
        senha=dados.get('senha')

        user = User.query.filter(User.usuário==usuário).first()
        if bcrypt.check_password_hash(user.senha,senha):
            login_user(user)
            return ('Logado')
        else:
            return 'nao autenticado'
    
    @app.route('/logout')
    def logout():
        logout_user()
        return 'Sucesso'
    
    @app.route('/createuser',methods=['POST'])
    def new_user():
        dados=request.get_json()
        usuário= dados.get('usuário')
        senha=dados.get('senha')

        hash_senha=bcrypt.generate_password_hash(senha)
        
        new_user=User(usuário=usuário,senha=hash_senha)
        db.session.add(new_user)
        db.session.commit()
        return 'Criado'