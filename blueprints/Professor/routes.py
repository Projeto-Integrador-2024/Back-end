from flask import Blueprint, request, jsonify
from blueprints.Professor.model import Professor, InvalidDataError
from blueprints.auth import professor_required
from flask_login import current_user, login_required

Professor_bp = Blueprint("Professor",__name__)

    
@Professor_bp.route('/PROFESSOR/CREATE/VAGA', methods=['POST'])
@professor_required 
def criar_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    dados = request.get_json()
    nova_vaga = Vaga(criador_id=current_user.ra, 
                     nome=dados['nome'],
                     descricao=dados['descricao'],
                     bolsa=dados['bolsa'],
                     bolsa_valor=dados['bolsa_valor'],
                     tipo=dados['tipo'],
                     )
    db.session.add(nova_vaga)
    db.session.commit()
    return jsonify({"sucesso": "Vaga criada com sucesso"}), 201

    
@Professor_bp.route('/PROFESSOR/DELETE/VAGA', methods=['DELETE'])
@professor_required 
def del_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()

    if vaga.criador_id==current_user.ra: 
        db.session.delete(vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga deletada com sucesso"}), 201

@Professor_bp.route('/PROFESSOR/GET_MY/VAGA', methods=['GET'])
@professor_required
def get_my_vagas():
    from blueprints.Vagas.model import Vaga
    vagas = Vaga.query.filter_by(criador_id=current_user.ra).all()
    # Converte cada instância de vaga em um dicionário com todos os atributos
    result = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "valor": vaga.valor_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        } for vaga in vagas
    ]
    return jsonify(result), 200

@Professor_bp.route('/PROFESSOR/GET_ALL/VAGA', methods=['GET'])
@professor_required
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
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        } for vaga in vagas
    ]
    return jsonify(result), 200

@Professor_bp.route('/PROFESSOR/GET_BY_ID/VAGA', methods=['GET'])
@professor_required 
def get_vaga_by_id():
    from blueprints.Vagas.model import Vaga
    from app import db
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        result={
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "valor":vaga.valor_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        }
        return jsonify(result), 200
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404

@Professor_bp.route('/PROFESSOR/UPDATE/VAGA', methods=['PUT'])
@professor_required
def update_vaga():
    from extensions import db
    from blueprints.Vagas.model import Vaga
    dados = request.get_json()
    id = dados['id']
    vaga = Vaga.query.filter_by(id=id).first()
    
    if vaga is None:
        return jsonify({"ERRO": "Vaga não encontrada"}), 404

    # Certifique-se de que o professor que está atualizando a vaga é o criador
    if vaga.criador_id != current_user.ra:
        return jsonify({"ERRO": "Acesso negado: Você não tem permissão para atualizar esta vaga"}), 403

    # Atualize os campos conforme necessário
    vaga.nome = dados.get('nome', vaga.nome)
    vaga.descricao = dados.get('descricao', vaga.descricao)
    vaga.bolsa = dados.get('bolsa', vaga.bolsa)
    vaga.bolsa_valor = dados.get('bolsa_valor', vaga.bolsa_valor)
    vaga.tipo = dados.get('tipo', vaga.tipo)
    
    db.session.commit()
    
    return jsonify({"SUCESSO": "VAGA FOI ATUALIZADA"})


# @Professor_bp.route('/PROFESSOR/IMPORT/CSV', methods=['POST'])
# @professor_required
# def import_csv():
#     from flask_login import current_user 
#     from extensions import db
#     from blueprints.Vagas.model import Vaga
#     import pandas as pd

#     if not current_user.is_authenticated:
#         print("Usuário não autenticado no início da função")
#         return jsonify({"ERRO": "Usuário não autenticado"}), 403
#     print(f"Usuário autenticado: {current_user.ra}")

#     file = request.files.get('file')
#     if not file:
#         print("Nenhum arquivo fornecido")
#         return jsonify({"ERRO": "Nenhum arquivo fornecido"}), 400

#     try:
#         data = pd.read_csv(file)
#         print(data.head())  # Exibir as primeiras linhas para verificação
#     except Exception as e:
#         print(f"Erro ao ler o CSV: {e}")
#         return jsonify({"ERRO": f"Erro ao ler o arquivo CSV: {str(e)}"}), 400

#     try:
#         for index, row in data.iterrows():
#             vaga = Vaga(
#                 criador_id=row['criador_id'],
#                 nome=row['nome'],
#                 descricao=row['descricao'],
#                 bolsa=int(row['bolsa']),
#                 bolsa_valor=row['bolsa_valor'],
#                 tipo=int(row['tipo'])
#             )
#             db.session.add(vaga)
#         db.session.commit()
#         print("Dados importados com sucesso!")
#     except Exception as e:
#         db.session.rollback()
#         print(f"Erro ao importar dados: {e}")
#         return jsonify({"ERRO": f"Erro ao importar dados: {str(e)}"}), 500

#     return jsonify({"SUCESSO": "Dados importados com sucesso!"}), 200




