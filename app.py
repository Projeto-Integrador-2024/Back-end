from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

from blueprints.ADMIN.model import ADM
from blueprints.Aluno.model import Aluno
from blueprints.Professor.model import Professor
from datetime import timedelta
import pandas as pd
from blueprints.Vagas.model import Vaga
from blueprints.Professor.model import Professor

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
    user = Professor.query.filter(Professor.SIAPE==user_id).first()
    if user:
        print(f"Usuário carregado como Professor: {user}")
        return user
    print("Usuário não encontrado")
    return None


bcrypt = Bcrypt(app)

#REGISTRO DAS BLUEPRINTS:
from blueprints.Aluno.routes import Aluno_bp
app.register_blueprint(Aluno_bp)

from blueprints.Professor.routes import Professor_bp
app.register_blueprint(Professor_bp)

from blueprints.ADMIN.routes import ADM_bp
app.register_blueprint(ADM_bp)

#ROTAS GERAIS:
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

    # Inicializa a variável `user` como None
    user = None

    # Verifica se o usuário é um Aluno
    user = Aluno.query.filter(Aluno.ra == username).first()

    # Se `user` ainda for None, verifica se é um Professor
    if not user:
        user = Professor.query.filter(Professor.SIAPE == username).first()

    # Se `user` ainda for None, verifica se é um ADM
    if not user:
        user = ADM.query.filter(ADM.username == username).first()

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
                tipo=int(row['tipo']),
            )
            db.session.add(vaga)
        db.session.commit()
        print("Dados importados com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar dados: {e}")
        return jsonify({"ERRO": f"Erro ao importar dados: {str(e)}"}), 500

    return jsonify({"SUCESSO": "Dados importados com sucesso!"}), 200

@app.route('/csv_professores',methods=['POST'])
def import_csv_professores():
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
            professor = Professor(
                SIAPE=str(row['SIAPE']),
                nome=str(row['nome']),
                cpf=str(row['cpf']),
                senha=str(row['senha']),
            )
            db.session.add(professor)
        db.session.commit()
        print("Dados importados com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao importar dados: {e}")
        return jsonify({"ERRO": f"Erro ao importar dados: {str(e)}"}), 500

    return jsonify({"SUCESSO": "Dados importados com sucesso!"}), 200

@app.route('/GET_ALL_VAGAS',methods=['GET'])
def get_all_vagas():
    from blueprints.Vagas.model import Vaga
    vagas = Vaga.query.all()
    result = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "valor":vaga.valor_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "criador_nome": vaga.criador.nome if vaga.criador else "Desconhecido",
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        } for vaga in vagas
    ]
    return jsonify(result), 200

@app.route('/GET_VAGAS_BY_ID',methods=['GET'])
def get_vaga_by_code():
    from blueprints.Vagas.model import Vaga
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        result={
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "valor":vaga.valor_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador.SIAPE,
            "criador_nome":vaga.criador.nome,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        }
        return jsonify(result), 200
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404

@app.route('/CRIAR_TESTE', methods=['POST'])
def criar_instancias_teste():

    senha = 'senha_teste'
    Hash_da_senha = bcrypt.generate_password_hash(senha)
    
    novo_admin = ADM(nome="Admin_Teste",cpf="12312312312", username="teste", senha = Hash_da_senha)
    novo_aluno = Aluno(ra="a0000000",nome="Aluno_Teste",periodo=1,cpf="12312312312", senha = Hash_da_senha)
    novo_professor = Professor(SIAPE="0000000",nome="Professor_Teste",cpf="12312312312", senha = Hash_da_senha)
    db.session.add(novo_admin)
    db.session.add(novo_aluno)
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({"sucesso": "instancias adicionadas com sucesso"})

@app.route('/CADASTRO_ALUNO', methods=['POST'])
def cadastro_aluno():
    dados = request.get_json()
    Hash_da_senha = bcrypt.generate_password_hash(dados['senha'])
    novo_aluno = Aluno(dados['ra'],dados['nome'], dados['periodo'], dados['cpf'], Hash_da_senha)
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"sucesso": "cadastro realizado com sucesso"})

@app.route('/CADASTRO_PROFESSOR', methods=['POST'])
def cadastro_prof():
    dados = request.get_json()
    Hash_da_senha = bcrypt.generate_password_hash(dados['senha'])
    novo_prof = Professor(dados['SIAPE'],dados['nome'], dados['cpf'],Hash_da_senha)
    db.session.add(novo_prof)
    db.session.commit()
    return jsonify({"sucesso": "cadastro realizado com sucesso"})


if __name__ == '__main__':
    app.run(debug=True)
