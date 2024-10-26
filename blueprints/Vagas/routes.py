from flask import Blueprint, request, jsonify
from blueprints.Vagas.model import Vaga, InvalidDataError


Vagas_bp = Blueprint("Vagas",__name__)


@Vagas_bp.route('/VAGA/CREATE', methods=['POST'])
def criar_vaga():
    from app import db
    dados = request.get_json()
    nome = dados.get('nome')
    descricao = dados.get('descricao')
    bolsa = dados.get('bolsa')
    tipo = dados.get('tipo')
    try:
        new_vaga = Vaga(nome=nome, descricao=descricao, bolsa=bolsa, tipo=tipo)
        db.session.add(new_vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga criada com sucesso"})
    except InvalidDataError as e:
            return jsonify({"ERRO": e.message}), 400

@Vagas_bp.route('/VAGA/GET_ALL', methods=['GET'])
def get_all_vagas():
    vagas = Vaga.query.all()
    result = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "tipo":vaga.check_tipo(),
        } for vaga in vagas
    ]
    return jsonify(result), 200

@Vagas_bp.route('/VAGA/DELETE', methods=['DELETE'])
def deletar_vaga():
    from app import db
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        db.session.delete(vaga)
        db.session.commit()
        return jsonify({"sucesso": f"Vaga com id:{id} foi deletado com sucesso"}), 200
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404

@Vagas_bp.route('/VAGA/GET_BY_CODIGO', methods=['GET'])
def get_vaga_by_code():
    from app import db
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        result={
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "tipo":vaga.check_tipo(),
        }
        return jsonify(result), 200
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404
    
@Vagas_bp.route('/VAGA/UPDATE', methods=['PUT'])
def atualizar_vaga():
    from app import db
    dados = request.get_json()
    id = dados.get('id')
    nome = dados.get('nome')
    descricao = dados.get('descricao')
    bolsa = dados.get('bolsa')
    tipo = dados.get('tipo')

    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        vaga.nome = nome
        vaga.descricao = descricao
        vaga.bolsa = bolsa
        vaga.tipo = tipo
        db.session.commit()
        return jsonify({"Sucesso": f"Vaga com id: {id} atualizada"})
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404