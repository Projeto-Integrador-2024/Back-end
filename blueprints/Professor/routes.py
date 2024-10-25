from flask import Blueprint, request, jsonify
from blueprints.Professor.model import Professor, InvalidDataError

Professor_bp = Blueprint("Professor",__name__)


@Professor_bp.route('/PROFESSOR/CREATE', methods=['POST'])
def criar_prof():
    from app import db
    dados = request.get_json()
    try:
        novo_prof = Professor(dados['nome'], dados['cpf'])
        db.session.add(novo_prof)
        db.session.commit()
        return jsonify({"sucesso": "Professor adicionado com sucesso"})
    except InvalidDataError as e:
            return jsonify({"ERRO": e.message}), 400

@Professor_bp.route('/PROFESSOR/GET_ALL', methods=['GET'])
def get_all_profs():
    profs = Professor.query.all()
    result = [
        {
            "ra": prof.ra,
            "nome": prof.nome,
            "cpf": prof.cpf
        } for prof in profs
    ]
    return jsonify(result), 200

@Professor_bp.route('/PROFESSOR/DELETE', methods=['DELETE'])
def deletar_prof():
    from app import db
    dados = request.get_json()
    ra = dados.get('ra')
    prof = Professor.query.filter_by(ra=ra).first()
    if prof:
        db.session.delete(prof)
        db.session.commit()
        return jsonify({"sucesso": f"Professor com RA {ra} foi deletado com sucesso"}), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404

@Professor_bp.route('/PROFESSOR/GET_BY_RA', methods=['GET'])
def get_prof_by_ra():
    dados = request.get_json()
    ra = dados.get('ra')

    try:
        prof = Professor.query.filter_by(ra=ra).first()
        if prof:
            result = {
                "ra": prof.ra,
                "nome": prof.nome,
                "cpf": prof.cpf
            }
            return jsonify(result), 200
        else:
            return jsonify({"erro": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@Professor_bp.route('/PROFESSOR/UPDATE', methods=['PUT'])
def atualizar_prof():
    from app import db
    dados = request.get_json()
    ra = dados.get('ra')
    nome = dados.get('nome')
    cpf = dados.get('cpf')

    prof = Professor.query.filter_by(ra=ra).first()
    if prof:
        prof.nome = nome
        prof.cpf = cpf
        db.session.commit()
        return jsonify({"sucesso": f"Professor com RA {ra} foi atualizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404
