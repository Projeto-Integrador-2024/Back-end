from flask import Flask, request
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

from blueprints.ADMIN.model import ADM
from blueprints.Aluno.model import Aluno
from blueprints.Professor.model import Professor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./SISUNI.db'
app.secret_key = 'SOME_KEY'

#Iniciando Banco de dados e CORS:
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

#Iniciando pacote de login e função de autenticação: 
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Tente carregar como Administrador
    user = ADM.query.filter(ADM.adm_id==user_id).first()
    if not user:
        # Se não for Administrador, tente carregar como Aluno
        user = Aluno.query.filter(Aluno.ra==user_id).first()
    if not user:
        # Se não for Aluno, tente carregar como Professor
        user = Professor.query.filter(Professor.ra==user_id).first()
    return user

bcrypt = Bcrypt(app)

#REGISTRO DAS BLUEPRINTS:
from blueprints.Aluno.routes import Aluno_bp
app.register_blueprint(Aluno_bp)

from blueprints.Vagas.routes import Vagas_bp
app.register_blueprint(Vagas_bp)

from blueprints.Professor.routes import Professor_bp
app.register_blueprint(Professor_bp)

from blueprints.ADMIN.routes import ADM_bp
app.register_blueprint(ADM_bp)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return str(current_user.username)
    else:
        return 'No user is logged in'

@app.route('/login',methods=['POST'])
def login():
    dados = request.get_json()
    username = dados['username']
    senha = dados['senha']
    if username[0].lower() == 'a':
        user = Aluno.query.filter(Aluno.ra==username).first()
    elif username[0].lower() == 'p':
        user = Professor.query.filter(Professor.ra==username).first()
    else:
        user = ADM.query.filter(ADM.username==username).first()

    if bcrypt.check_password_hash(user.senha, senha):
        login_user(user)
        return f"sucesso, olá {user.nome}"
    else:
        return "ERRO"
    
@app.route('/logout')
def logout():
    logout_user()
    return "sucesso"

if __name__ == '__main__':
    app.run(debug=True)
