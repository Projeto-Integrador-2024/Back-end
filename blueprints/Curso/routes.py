from flask import Blueprint, request, jsonify
from blueprints.Curso.model import Curso
from app import db


Curso_bp = Blueprint("Curso",__name__)


@Curso_bp.route('/CURSO/CREATE', methods=['POST'])
def criar_curso():
    pass

@Curso_bp.route('/CURSO/GET_ALL', methods=['GET'])
def get_all_curso():
    pass

@Curso_bp.route('/CURSO/DELETE', methods=['DELETE'])
def deletar_curso():
    pass

@Curso_bp.route('/CURSO/GET_BY_CODIGO', methods=['GET'])
def get_curso_by_code():
    pass
    
@Curso_bp.route('/CURSO/UPDATE', methods=['PUT'])
def atualizar_curso():
    pass