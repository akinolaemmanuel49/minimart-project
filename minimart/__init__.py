from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from minimart.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.login_message = 'You need to be signed in to view this page.'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)

    from minimart.models import db
    db.init_app(app)

    from minimart.pages import pages
    app.register_blueprint(pages)

    from minimart.auth import auth
    app.register_blueprint(auth)
    return app


app = create_app()
app.app_context().push()