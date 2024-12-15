from functools import wraps
from flask import Blueprint, request, jsonify

#Import das classes:
from blueprints.Aluno.model import Aluno
from blueprints.Professor.model import Professor
from blueprints.Vagas.model import Vaga

from blueprints.auth import admin_required
ADM_bp = Blueprint("ADMIN",__name__)

@ADM_bp.route('/ADMIN/GET_ALL/ALUNO', methods=['GET'])
@admin_required
def get_all_alunos():
    alunos = Aluno.query.all()
    result = [
        {
            "ra": aluno.ra,
            "nome": aluno.nome,
            "periodo": aluno.periodo,
            "cpf": aluno.cpf,
            "vagas": [vaga.id for vaga in aluno.vagas]
        } for aluno in alunos
    ]
    return jsonify(result), 200

@ADM_bp.route('/ADMIN/DELETE/ALUNO', methods=['DELETE'])
@admin_required
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

@ADM_bp.route('/ADMIN/GET_BY_ID/ALUNO', methods=['GET'])
@admin_required
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
                "cpf": aluno.cpf,
                "vagas": [vaga.id for vaga in aluno.vagas]
            }
            return jsonify(result), 200
        else:
            return jsonify({"erro": "Aluno não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@ADM_bp.route('/ADMIN/UPDATE/ALUNO', methods=['PUT'])
@admin_required
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


@ADM_bp.route('/ADMIN/GET_ALL/PROFESSOR', methods=['GET'])
@admin_required
def get_all_profs():
    profs = Professor.query.all()
    result = [
        {
            "SIAPE": prof.SIAPE,
            "nome": prof.nome,
            "cpf": prof.cpf,
            "vagas_criadas": [vaga.id for vaga in prof.vagas_criadas]
        } for prof in profs
    ]
    return jsonify(result), 200

@ADM_bp.route('/ADMIN/DELETE/PROFESSOR', methods=['DELETE'])
@admin_required
def deletar_prof():
    from app import db
    dados = request.get_json()
    siape = dados.get('SIAPE')
    prof = Professor.query.filter_by(SIAPE=siape).first()
    if prof:
        db.session.delete(prof)
        db.session.commit()
        return jsonify({"sucesso": f"Professor com SIAPE: {siape} foi deletado com sucesso"}), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404

@ADM_bp.route('/ADMIN/GET_BY_ID/PROFESSOR', methods=['GET'])
@admin_required
def get_prof_by_ra():
    dados = request.get_json()
    siape = dados.get('SIAPE')

    try:
        prof = Professor.query.filter_by(SIAPE=siape).first()
        if prof:
            result = {
                "SIAPE": prof.SIAPE,
                "nome": prof.nome,
                "cpf": prof.cpf,
                "vagas_criadas": [vaga.id for vaga in prof.vagas_criadas]
            }
            return jsonify(result), 200
        else:
            return jsonify({"erro": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@ADM_bp.route('/ADMIN/UPDATE/PROFESSOR', methods=['PUT'])
@admin_required
def atualizar_prof():
    from app import db
    dados = request.get_json()
    siape = dados.get('SIAPE')
    nome = dados.get('nome')
    cpf = dados.get('cpf')

    prof = Professor.query.filter_by(SIAPE=siape).first()
    if prof:
        prof.nome = nome
        prof.cpf = cpf
        db.session.commit()
        return jsonify({"sucesso": f"Professor com SIAPE {siape} foi atualizado com sucesso"}), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404

@ADM_bp.route('/ADMIN/CREATE/VAGA', methods=['POST'])
@admin_required
def criar_vaga():
    from app import db
    dados = request.get_json()
    nome = dados.get('nome')
    descricao = dados.get('descricao')
    bolsa = dados.get('bolsa')
    bolsa_valor = dados.get('bolsa_valor')
    tipo = dados.get('tipo')
    criador_id = dados.get('criador_id')

    prof = Professor.query.filter_by(SIAPE=criador_id).first()
    if prof:
        new_vaga = Vaga(nome=nome, descricao=descricao, bolsa=bolsa, bolsa_valor=bolsa_valor, tipo=tipo, criador_id = criador_id)
        db.session.add(new_vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga criada com sucesso"})
    else:
        return jsonify({"ERRO": "Professor não encontrado"})


@ADM_bp.route('/ADMIN/DELETE/VAGA', methods=['DELETE'])
@admin_required
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

    
@ADM_bp.route('/ADMIN/UPDATE/VAGA', methods=['PUT'])
@admin_required
def atualizar_vaga():
    from app import db
    dados = request.get_json()
    id = dados.get('id')
    nome = dados.get('nome')
    descricao = dados.get('descricao')
    bolsa = dados.get('bolsa')
    bolsa_valor = dados.get('bolsa_valor')
    tipo = dados.get('tipo')

    vaga = Vaga.query.filter_by(id=id).first()
    if vaga:
        vaga.nome = nome
        vaga.descricao = descricao
        vaga.bolsa = bolsa
        vaga.bolsa_valor = bolsa_valor
        vaga.tipo = tipo
        db.session.commit()
        return jsonify({"Sucesso": f"Vaga com id: {id} atualizada"})
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404