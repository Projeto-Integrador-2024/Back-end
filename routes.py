from flask import request,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import Aluno, Professor, Curso 

def register_routes(app, db):
    @app.route('/ALUNO/CREATE', methods=['POST'])
    def criar_aluno():
        dados = request.get_json()
        nome = dados.get('nome')
        periodo = int(dados.get('periodo'))
        cpf = dados.get('cpf')

        new_aluno = Aluno(nome=nome, periodo=periodo, cpf=cpf)
        db.session.add(new_aluno)
        db.session.commit()
        return jsonify({"sucesso": "Aluno adicionado com sucesso"})

    @app.route('/ALUNO/GET_ALL', methods=['GET'])
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
    
    @app.route('/ALUNO/DELETE', methods=['DELETE'])
    def deletar_aluno():
        dados = request.get_json()
        ra = dados.get('ra')
        aluno = Aluno.query.filter_by(ra=ra).first()
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return jsonify({"sucesso": f"Aluno com RA {ra} foi deletado com sucesso"}), 200
        else:
            return jsonify({"erro": "Aluno não encontrado"}), 404

    @app.route('/ALUNO/GET_BY_RA', methods=['GET'])
    def get_by_ra():
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
        
    @app.route('/ALUNO/UPDATE', methods=['PUT'])
    def atualizar_aluno():
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



    # @app.route('/logout')
    # def logout():
    #     logout_user()
    #     return 'Sucesso'
    
    # @app.route('/createuser',methods=['POST'])
    # def new_user():
    #     dados=request.get_json()
    #     usuario= dados.get('usuario')
    #     senha=dados.get('senha')

    #     hash_senha=bcrypt.generate_password_hash(senha)
        
    #     new_user=User(usuario=usuario,senha=hash_senha)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return 'Criado'