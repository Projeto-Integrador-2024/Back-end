from flask import Blueprint, request, jsonify
from blueprints.Professor.model import Professor, InvalidDataError
from blueprints.auth import professor_required

Professor_bp = Blueprint("Professor",__name__)
    
@Professor_bp.route('/PROFESSOR/CREATE/VAGA', methods=['POST'])
@professor_required 
def criar_vaga():
    dados = request.get_json()
    #Body da requisição:
    #RA do professor
    ra = dados.get('ra')
    #parametros para criar vaga:
    nome=dados.get('nome')
    descricao=dados.get('descricao')
    bolsa=dados.get('bolsa')
    tipo=dados.get('tipo')

    prof = Professor.query.filter_by(ra=ra).first()
    
    if not prof: 
        return jsonify({"ERRO": "Professor não encontrado"}), 404 
    try: 
        mensagem = prof.criar_vaga(nome, descricao, bolsa, tipo) 
        return jsonify({"sucesso": mensagem}), 201 
    except InvalidDataError as e: 
        return jsonify({"ERRO": e.message}), 400 
    except Exception as e: 
        return jsonify({"ERRO": str(e)}), 500
    
@Professor_bp.route('/PROFESSOR/DELETE/VAGA', methods=['DELETE'])
@professor_required 
def del_vaga():
    dados = request.get_json()
    id = dados.get('id')
    try: 
        mensagem = Professor.deletar_vaga(id) 
        return jsonify({"sucesso": mensagem}) 
    except Exception as e: 
        return jsonify({"ERRO": str(e)}), 400 