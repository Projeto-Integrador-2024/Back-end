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
            "id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "tipo": vaga.check_tipo(),
        }
        vagas_json.append(vaga_dict)

    return jsonify(vagas_json)

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
    #Body da requisição:
    id_vaga = dados.get('id')

    aluno = Aluno.query.filter_by(ra=current_user.ra).first()
    vaga = Vaga.query.filter_by(id=id_vaga).first()

    aluno.vagas.remove(vaga)
    db.session.commit()
    return jsonify({"sucesso": 'desinscrito com sucesso'}) 

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

# ---------------------------------------------
# ROTA PARA FAVORITAR UMA VAGA
# ---------------------------------------------
@Aluno_bp.route('/ALUNO/FAVORITAR_VAGA', methods=['POST'])
@aluno_required
def favoritar_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    if not isinstance(current_user, Aluno):
        return jsonify({"erro": "Acesso negado: Apenas alunos podem favoritar vagas"}), 403
    
    dados = request.get_json()
    id_vaga = dados.get('id_vaga')

    vaga = Vaga.query.get(id_vaga)
    if not vaga:
        return jsonify({"erro": "Vaga não encontrada"}), 404

    if vaga not in current_user.vagas_favoritadas:
        current_user.vagas_favoritadas.append(vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga favoritada com sucesso!"}), 200
    else:
        return jsonify({"erro": "Vaga já favoritada"}), 400

# ---------------------------------------------
# ROTA PARA DESFAVORITAR UMA VAGA
# ---------------------------------------------
@Aluno_bp.route('/ALUNO/DESFAVORITAR_VAGA', methods=['POST'])
@aluno_required
def desfavoritar_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    if not isinstance(current_user, Aluno):
        return jsonify({"erro": "Acesso negado: Apenas alunos podem desfavoritar vagas"}), 403
    
    dados = request.get_json()
    id_vaga = dados.get('id_vaga')

    vaga = Vaga.query.get(id_vaga)
    if not vaga:
        return jsonify({"erro": "Vaga não encontrada"}), 404

    if vaga in current_user.vagas_favoritadas:
        current_user.vagas_favoritadas.remove(vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga removida dos favoritos com sucesso!"}), 200
    else:
        return jsonify({"erro": "Vaga não estava favoritada"}), 400

# ---------------------------------------------
# ROTA PARA OBTER TODAS AS VAGAS FAVORITADAS
# ---------------------------------------------
@Aluno_bp.route('/ALUNO/GET_FAVORITADAS', methods=['GET'])
@aluno_required
def get_favoritadas():
    if not isinstance(current_user, Aluno):
        return jsonify({"erro": "Acesso negado: Apenas alunos podem acessar essa informação"}), 403
    
    vagas_favoritadas = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "tipo": vaga.tipo,
            "bolsa": vaga.bolsa,
            "valor_bolsa": vaga.bolsa_valor
        }
        for vaga in current_user.vagas_favoritadas
    ]
    
    return jsonify(vagas_favoritadas), 200
