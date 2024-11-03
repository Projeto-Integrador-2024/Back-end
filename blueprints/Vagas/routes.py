from flask import Blueprint, request, jsonify
from blueprints.Vagas.model import Vaga, InvalidDataError

Vagas_bp = Blueprint("Vagas",__name__)

