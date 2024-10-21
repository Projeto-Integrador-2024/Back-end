from flask import Blueprint, request, jsonify
from blueprints.Aluno.model import Aluno

Aluno_bp = Blueprint("Aluno",__name__)


@Aluno_bp.route('/ALUNO/CREATE', methods=['POST'])
def criar_aluno():
    from app import db
    dados = request.get_json()
    nome = dados.get('nome')
    periodo = int(dados.get('periodo'))
    cpf = dados.get('cpf')
    nome_do_curso = dados.get('nome_do_curso')

    new_aluno = Aluno(nome=nome, periodo=periodo, cpf=cpf, nome_do_curso=nome_do_curso)
    db.session.add(new_aluno)
    db.session.commit()
    return jsonify({"sucesso": "Aluno adicionado com sucesso"})

@Aluno_bp.route('/ALUNO/GET_ALL', methods=['GET'])
def get_all_alunos():
    alunos = Aluno.query.all()
    result = [
        {
            "ra": aluno.ra,
            "nome": aluno.nome,
            "periodo": aluno.periodo,
            "cpf": aluno.cpf
        } for aluno in alunos
    ]
    return jsonify(result), 200

@Aluno_bp.route('/ALUNO/DELETE', methods=['DELETE'])
def deletar_aluno():
    from app import db
    dados = request.get_json()
    ra = dados.get('ra')
    aluno = Aluno.query.filter_by(ra=ra).first()
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"sucesso": f"Aluno com RA {ra} foi deletado com sucesso"}), 200
    else:
        return jsonify({"erro": "Aluno não encontrado"}), 404

@Aluno_bp.route('/ALUNO/GET_BY_RA', methods=['GET'])
def get_aluno_by_ra():
    dados = request.get_json()
    ra = dados.get('ra')

    try:
        aluno = Aluno.query.filter_by(ra=ra).first()
        if aluno:
            result = {
                "ra": aluno.ra,
                "nome": aluno.nome,
                "periodo": aluno.periodo,
                "cpf": aluno.cpf
            }
            return jsonify(result), 200
        else:
            return jsonify({"erro": "Aluno não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@Aluno_bp.route('/ALUNO/UPDATE', methods=['PUT'])
def atualizar_aluno():
    from app import db
    dados = request.get_json()
    ra = dados.get('ra')
    nome = dados.get('nome')
    periodo = int(dados.get('periodo'))
    cpf = dados.get('cpf')

    aluno = Aluno.query.filter_by(ra=ra).first()
    if aluno:
        aluno.nome = nome
        aluno.periodo = periodo
        aluno.cpf = cpf
        db.session.commit()
        return jsonify({"sucesso": f"Aluno com RA {ra} foi atualizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Aluno não encontrado"}), 404
