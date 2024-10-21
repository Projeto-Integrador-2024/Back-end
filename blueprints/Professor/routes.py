from flask import Blueprint, request, jsonify
from blueprints.Professor.model import Professor
from app import db


Professor_bp = Blueprint("Professor",__name__)


@Professor_bp.route('/PROFESSOR/CREATE', methods=['POST'])
def criar_professor():
    pass

@Professor_bp.route('/PROFESSOR/GET_ALL', methods=['GET'])
def get_all_professor():
    pass

@Professor_bp.route('/PROFESSOR/DELETE', methods=['DELETE'])
def deletar_professor():
    pass

@Professor_bp.route('/PROFESSOR/GET_BY_RA', methods=['GET'])
def get_professor_by_ra():
    pass
    
@Professor_bp.route('/PROFESSOR/UPDATE', methods=['PUT'])
def atualizar_professor():
    pass