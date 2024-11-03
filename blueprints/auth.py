from functools import wraps
from flask import request, jsonify
from flask_login import current_user, login_required

def aluno_required(f):
    from blueprints.Aluno.model import Aluno
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and isinstance(current_user, Aluno):
            return f(*args, **kwargs)
        else:
            return jsonify({"ERRO": "Acesso negado: Requer aluno"}), 403
    return decorated_function

def professor_required(f):
    from blueprints.Professor.model import Professor
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and isinstance(current_user, Professor):
            return f(*args, **kwargs)
        else:
            return jsonify({"ERRO": "Acesso negado: Requer professor"}), 403
    return decorated_function

def admin_required(f):
    from blueprints.ADMIN.model import ADM
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and isinstance(current_user, ADM):
            return f(*args, **kwargs)
        else:
            return jsonify({"ERRO": "Acesso negado: Requer administrador"}), 403
    return decorated_function
