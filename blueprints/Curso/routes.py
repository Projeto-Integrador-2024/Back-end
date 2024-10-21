from flask import Blueprint, request, jsonify
from blueprints.Curso.model import Curso


Curso_bp = Blueprint("Curso",__name__)


@Curso_bp.route('/CURSO/CREATE', methods=['POST'])
def criar_curso():
    from app import db
    dados = request.get_json()
    codigo = dados.get('codigo')
    nome = dados.get('nome')

    new_curso = Curso(codigo=codigo,nome=nome)
    db.session.add(new_curso)
    db.session.commit()
    return jsonify({"sucesso": "Curso adicionado com sucesso"})

@Curso_bp.route('/CURSO/GET_ALL', methods=['GET'])
def get_all_curso():
    pass

@Curso_bp.route('/CURSO/DELETE', methods=['DELETE'])
def deletar_curso():
    from app import db
    dados = request.get_json()
    codigo = dados.get('codigo')
    curso = Curso.query.filter_by(codigo=codigo).first()
    if curso:
        db.session.delete(curso)
        db.session.commit()
        return jsonify({"sucesso": f"Curso com codigo {codigo} foi deletado com sucesso"}), 200
    else:
        return jsonify({"erro": "Curso não encontrado"}), 404

@Curso_bp.route('/CURSO/GET_BY_CODIGO', methods=['GET'])
def get_curso_by_code():
    pass
    
@Curso_bp.route('/CURSO/UPDATE', methods=['PUT'])
def atualizar_curso():
    pass