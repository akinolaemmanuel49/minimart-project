from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from minimart.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)

    from minimart.pages import pages
    app.register_blueprint(pages)

    from minimart.auth import auth
    app.register_blueprint(auth)
    return app
