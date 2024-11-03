from flask import Blueprint, request, jsonify
from blueprints.Aluno.model import Aluno, InvalidDataError

Aluno_bp = Blueprint("Aluno",__name__)

@Aluno_bp.route('/ALUNO/INSCREVER', methods=['POST'])
def increver():
    dados = request.get_json()
    #Body da requisição:
    ra = dados.get('ra')
    id_vaga = dados.get('id')

    aluno = Aluno.query.filter_by(ra=ra).first()
    
    try: 
        mensagem = aluno.increver(ra, id_vaga) 
        return jsonify({"sucesso": mensagem}) 
    except Exception as e: 
        return jsonify({"ERRO": str(e)}), 400 

@Aluno_bp.route('/ALUNO/DESINSCREVER', methods=['POST'])
def desinscrever():
    dados = request.get_json()
    #Body da requisição:
    ra = dados.get('ra')
    id_vaga = dados.get('id')

    aluno = Aluno.query.filter_by(ra=ra).first()
    
    try: 
        mensagem = aluno.desinscrever(ra, id_vaga) 
        return jsonify({"sucesso": mensagem}) 
    except Exception as e: 
        return jsonify({"ERRO": str(e)}), 400 