from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

from blueprints.ADMIN.model import ADM
from blueprints.Aluno.model import Aluno
from blueprints.Professor.model import Professor
from datetime import timedelta

from blueprints.auth import professor_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SOME_SECRET_KEY'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./SISUNI.db'

#Iniciando Banco de dados e CORS:
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

#Iniciando pacote de login e função de autenticação: 
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print(f"Tentando carregar usuário com ID: {user_id}")
    user = ADM.query.filter(ADM.adm_id==user_id).first()
    if user:
        print(f"Usuário carregado como ADM: {user}")
        return user
    user = Aluno.query.filter(Aluno.ra==user_id).first()
    if user:
        print(f"Usuário carregado como Aluno: {user}")
        return user
    user = Professor.query.filter(Professor.ra==user_id).first()
    if user:
        print(f"Usuário carregado como Professor: {user}")
        return user
    print("Usuário não encontrado")
    return None


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

@app.route('/csv',methods=['POST'])
def import_csv():
    from flask_login import current_user 
    from extensions import db
    from blueprints.Vagas.model import Vaga
    import pandas as pd

    file = request.files.get('file')
    if not file:
        print("Nenhum arquivo fornecido")
        return jsonify({"ERRO": "Nenhum arquivo fornecido"}), 400

    try:
        data = pd.read_csv(file)
        print(data.head())  # Exibir as primeiras linhas para verificação
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return jsonify({"ERRO": f"Erro ao ler o arquivo CSV: {str(e)}"}), 400

    try:
        for index, row in data.iterrows():
            vaga = Vaga(
                criador_id=row['criador_id'],
                nome=row['nome'],
                descricao=row['descricao'],
                bolsa=int(row['bolsa']),
                bolsa_valor=row['bolsa_valor'],
                tipo=int(row['tipo'])
            )
            db.session.add(vaga)
        db.session.commit()
        print("Dados importados com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar dados: {e}")
        return jsonify({"ERRO": f"Erro ao importar dados: {str(e)}"}), 500

    return jsonify({"SUCESSO": "Dados importados com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
