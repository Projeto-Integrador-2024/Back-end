from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./SISUNI.db'

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

#REGISTRO DAS BLUEPRINTS:
from blueprints.Aluno.routes import Aluno_bp
app.register_blueprint(Aluno_bp)

from blueprints.Vagas.routes import Vagas_bp
app.register_blueprint(Vagas_bp)

from blueprints.Professor.routes import Professor_bp
app.register_blueprint(Professor_bp)

if __name__ == '__main__':
    app.run(debug=True)
