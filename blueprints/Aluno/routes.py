from flask import Blueprint, request, jsonify
from blueprints.Aluno.model import Aluno, InvalidDataError
from blueprints.auth import aluno_required
from flask_login import current_user

Aluno_bp = Blueprint("Aluno",__name__)

@Aluno_bp.route('/ALUNO/INSCREVER', methods=['POST'])
@aluno_required 
def increver():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    dados = request.get_json()
    #Body da requisição:
    id_vaga = dados.get('id')

    aluno = Aluno.query.filter_by(ra=current_user.ra).first()
    vaga = Vaga.query.filter_by(id=id_vaga).first()

    aluno.vagas.append(vaga)
    db.session.commit()
    return jsonify({"sucesso": 'inscrito com sucesso'}) 

@Aluno_bp.route('/ALUNO/GET_ALL_VAGAS', methods=['GET'])
@aluno_required 
def get_all_vagas():
    from blueprints.Vagas.model import Vaga
    vagas = Vaga.query.all()
    result = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        } for vaga in vagas
    ]
    return jsonify(result), 200


@Aluno_bp.route('/ALUNO/GET_VAGAS_BY_ID', methods=['GET'])
@aluno_required 
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
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        }
        return jsonify(result), 200
    else:
        return jsonify({"erro": "Vaga não encontrada"}), 404

@Aluno_bp.route('/ALUNO/GET_MY_VAGAS', methods=['GET'])
@aluno_required 
def get_mine():
    from blueprints.Aluno.model import association_table
    from blueprints.Vagas.model import Vaga
    from extensions import db
# Obter o aluno atual
    aluno = Aluno.query.filter_by(ra=current_user.ra).first()

    # Fazer join entre a tabela de associações e a tabela Vaga
    results = db.session.query(Vaga).join(association_table, Vaga.id == association_table.c.vaga_id).filter(association_table.c.aluno_ra == aluno.ra).all()

    # Preparar os dados para retorno
    vagas_json = []
    for vaga in results:
        vaga_dict = {
            "id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "tipo": vaga.check_tipo(),
        }
        vagas_json.append(vaga_dict)

    return jsonify(vagas_json)


@Aluno_bp.route('/ALUNO/DESINSCREVER', methods=['POST'])
@aluno_required 
def desinscrever():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    dados = request.get_json()
    #Body da requisição:
    id_vaga = dados.get('id')

    aluno = Aluno.query.filter_by(ra=current_user.ra).first()
    vaga = Vaga.query.filter_by(id=id_vaga).first()

    aluno.vagas.remove(vaga)
    db.session.commit()
    return jsonify({"sucesso": 'desinscrito com sucesso'}) 