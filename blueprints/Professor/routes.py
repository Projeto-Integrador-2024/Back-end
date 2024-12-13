from flask import Blueprint, request, jsonify
from blueprints.auth import professor_required
from flask_login import current_user
from blueprints.Professor.model import Professor

Professor_bp = Blueprint("Professor",__name__)

    
@Professor_bp.route('/PROFESSOR/CREATE/VAGA', methods=['POST'])
@professor_required 
def criar_vaga():
    from blueprints.Vagas.model import Vaga
    from extensions import db
    dados = request.get_json()
    nova_vaga = Vaga(criador_id=current_user.SIAPE, 
                     nome=dados['nome'],
                     descricao=dados['descricao'],
                     bolsa=dados['bolsa'],
                     bolsa_valor=dados['bolsa_valor'],
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
    id = request.get_json().get('id')
    vaga = Vaga.query.filter_by(id=id).first()

    if vaga.criador_id==current_user.SIAPE: 
        db.session.delete(vaga)
        db.session.commit()
        return jsonify({"sucesso": "Vaga deletada com sucesso"}), 201

@Professor_bp.route('/PROFESSOR/GET_MY/VAGA', methods=['GET'])
@professor_required
def get_my_vagas():
    from blueprints.Vagas.model import Vaga
    vagas = Vaga.query.filter_by(criador_id=current_user.SIAPE).all()
    # Converte cada instância de vaga em um dicionário com todos os atributos
    result = [
        {
            "vaga_id": vaga.id,
            "nome": vaga.nome,
            "descricao": vaga.descricao,
            "bolsa": vaga.check_bolsa(),
            "valor": vaga.valor_bolsa(),
            "tipo":vaga.check_tipo(),
            "criador_id":vaga.criador_id,
            "incritos": [aluno.ra for aluno in vaga.candidatos]
        } for vaga in vagas
    ]
    return jsonify(result), 200


@Professor_bp.route('/PROFESSOR/UPDATE/VAGA', methods=['PUT'])
@professor_required
def update_vaga():
    from extensions import db
    from blueprints.Vagas.model import Vaga
    dados = request.get_json()
    id = dados['id']
    vaga = Vaga.query.filter_by(id=id).first()
    
    if vaga is None:
        return jsonify({"ERRO": "Vaga não encontrada"}), 404

    # Certifique-se de que o professor que está atualizando a vaga é o criador
    if vaga.criador_id != current_user.SIAPE:
        return jsonify({"ERRO": "Acesso negado: Você não é o criador dessa vaga"}), 403

    # Atualize os campos conforme necessário
    vaga.nome = dados.get('nome', vaga.nome)
    vaga.descricao = dados.get('descricao', vaga.descricao)
    vaga.bolsa = dados.get('bolsa', vaga.bolsa)
    vaga.bolsa_valor = dados.get('bolsa_valor', vaga.bolsa_valor)
    vaga.tipo = dados.get('tipo', vaga.tipo)
    
    db.session.commit()
    
    return jsonify({"SUCESSO": "VAGA FOI ATUALIZADA"})


@Professor_bp.route('/PROFESSOR/ATUALIZAR', methods=['PUT'])
@professor_required
def update_perfil_professor():
    from app import bcrypt
    from extensions import db
    dados = request.get_json()

    Hash_da_senha = bcrypt.generate_password_hash(dados['senha'])
    professor = Professor.query.filter_by(SIAPE=current_user.SIAPE).first()
    professor.SIAPE = dados.get('SIAPE')
    professor.nome = dados.get('nome')
    professor.cpf = dados.get('cpf')
    professor.senha = Hash_da_senha

    db.session.commit()
    return jsonify({"sucesso": 'dados atualizados com sucesso'}) 


