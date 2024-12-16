from flask import Blueprint, request, jsonify
from blueprints.Aluno.model import Aluno
from blueprints.auth import aluno_required
from flask_login import current_user

Aluno_bp = Blueprint("Aluno",__name__)

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
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.bolsa,
            "bolsa_valor": vaga.bolsa_valor,
            "tipo": vaga.tipo,
        }
        vagas_json.append(vaga_dict)

    return jsonify(vagas_json), 200


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

@Aluno_bp.route('/ALUNO/DESINSCREVER', methods=['POST'])
@aluno_required 
def desinscrever():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    dados = request.get_json()
    id_vaga = dados.get('id')

    print(f"Request data: {dados}")

    aluno = Aluno.query.filter_by(ra=current_user.ra).first()
    vaga = Vaga.query.filter_by(id=id_vaga).first()

    print(f"Dados recebidos: id_vaga={id_vaga}, aluno_ra={current_user.ra}")
    print(f"Aluno encontrado: {aluno}")
    print(f"Vaga encontrada: {vaga}")

    if not aluno or not vaga:
        print("Aluno ou Vaga não encontrados")
        return jsonify({"erro": "Aluno ou Vaga não encontrados"}), 404

    print(f"Tentando desinscrever {aluno.ra} da vaga {vaga.id}")

    if vaga not in aluno.vagas:
        print(f"O aluno {aluno.ra} não está inscrito na vaga {vaga.id}")
        return jsonify({"erro": "O aluno não está inscrito nesta vaga"}), 400

    aluno.vagas.remove(vaga)
    try:
        db.session.commit()
        print(f"Aluno {aluno.ra} desinscrito da vaga {vaga.id} com sucesso")
        return jsonify({"sucesso": 'Desinscrito com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao desinscrever da vaga: {str(e)}")
        return jsonify({"erro": "Erro ao desinscrever da vaga", "detalhes": str(e)}), 500



@Aluno_bp.route('/ALUNO/ATUALIZAR', methods=['PUT'])
@aluno_required 
def update_perfil_aluno():
    from extensions import db
    from app import bcrypt
    dados = request.get_json()

    Hash_da_senha = bcrypt.generate_password_hash(dados['senha'])
    aluno = Aluno.query.filter_by(ra=current_user.ra).first()
    aluno.ra = dados.get('ra')
    aluno.nome = dados.get('nome')
    aluno.periodo = dados.get('periodo')
    aluno.cpf = dados.get('cpf')
    aluno.senha = Hash_da_senha

    db.session.commit()
    return jsonify({"sucesso": 'dados atualizados com sucesso'}) 