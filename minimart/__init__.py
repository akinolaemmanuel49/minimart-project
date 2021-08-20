from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_seasurf import SeaSurf
from flask_migrate import Migrate

from minimart.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.login_message = 'You need to be signed in to view this page.'
bcrypt = Bcrypt()
csrf = SeaSurf()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from minimart.models import login_manager
    login_manager.init_app(app)

    csrf.init_app(app)

    from minimart.models import db
    db.init_app(app)

    migrate.init_app(app, db)

    from minimart.pages import pages
    app.register_blueprint(pages)

    from minimart.auth import auth
    app.register_blueprint(auth)

    from minimart.dashboard import dashboard
    app.register_blueprint(dashboard)

    from minimart.products import products
    app.register_blueprint(products)

    return app


app = create_app()
app.app_context().push()
