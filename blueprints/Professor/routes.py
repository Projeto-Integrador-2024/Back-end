from flask import Blueprint, request, jsonify
from blueprints.Professor.model import Professor, InvalidDataError
from blueprints.auth import professor_required
from flask_login import current_user

Professor_bp = Blueprint("Professor",__name__)

    
@Professor_bp.route('/PROFESSOR/CREATE/VAGA', methods=['POST'])
@professor_required 
def criar_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    dados = request.get_json()
    nova_vaga = Vaga(criador_id=current_user.ra, 
                     nome=dados['nome'],
                     descricao=dados['descricao'],
                     bolsa=dados['bolsa'],
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
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    dados = request.get_json()
    vaga = Vaga(criador_id=['criador_id'],
                id=dados['id'], 
                )
    if vaga.criador_id==current_user.ra: 
        db.session.delete(vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga deletada com sucesso"}), 201

@Professor_bp.route('/PROFESSOR/GET_MY/VAGA', methods=['GET'])
@professor_required
def get_my_vagas():
    from blueprints.Vagas.model import Vaga
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    vagas = Vaga.query.filter_by(criador_id=current_user.ra).all()
    # Converte cada instância de vaga em um dicionário com todos os atributos
    vagas_json = []
    for vaga in vagas:
        vaga_dict = {
            "id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa,
            "tipo": vaga.check_tipo,
            "criador_id": vaga.criador_id
        }
        vagas_json.append(vaga_dict)

    return jsonify(vagas_json) 

@Professor_bp.route('/PROFESSOR/GET_ALL/VAGA', methods=['GET'])
@professor_required
def get_all_vaga():
    from blueprints.Vagas.model import Vaga
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    vagas = Vaga.query.all()
    # Converte cada instância de vaga em um dicionário com todos os atributos
    vagas_json = []
    for vaga in vagas:
        vaga_dict = {
            "id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa,
            "tipo": vaga.check_tipo,
        }
        vagas_json.append(vaga_dict)

    return jsonify(vagas_json)


@Professor_bp.route('/PROFESSOR/GET_BY_ID/VAGA', methods=['GET'])
@professor_required 
def get_vaga_by_id():
    from blueprints.Vagas.model import Vaga
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    dados = request.get_json()
    id=dados['id'],
    vaga = Vaga.query.filter(Vaga.id == id).first()
    vaga_dict = {
            "id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa,
            "tipo": vaga.check_tipo,
        }
    return jsonify(vaga_dict)

@Professor_bp.route('/PROFESSOR/UPDATE/VAGA', methods=['PUT'])
@professor_required
def update_vaga():
    from extensions import db
    from blueprints.Vagas.model import Vaga
    if not isinstance(current_user, Professor):
        return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
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
    vaga.tipo = dados.get('tipo', vaga.tipo)
    
    db.session.commit()
    
    return jsonify({
        "id": vaga.id,
        "nome": vaga.nome,
        "descricao": vaga.descricao,
        "bolsa": vaga.bolsa,
        "tipo": vaga.tipo,
        "criador_id": vaga.criador_id
    }), 200
