from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///./SISUNI.db'

    db.init_app(app)

    from routes import register_routes
    register_routes(app,db)

    migrate=Migrate(app,db)
    return app