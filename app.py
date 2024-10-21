from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./SISUNI.db'
    db.init_app(app)
    
    from blueprints.Aluno.routes import Aluno_bp
    app.register_blueprint(Aluno_bp)

    from blueprints.Curso.routes import Curso_bp
    app.register_blueprint(Curso_bp)

    from blueprints.Professor.routes import Professor_bp
    app.register_blueprint(Professor_bp)

    migrate=Migrate(app,db)
    return app