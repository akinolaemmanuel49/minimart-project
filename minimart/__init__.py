from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_seasurf import SeaSurf
from flask_migrate import Migrate
from flask_mail import Mail
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

from minimart.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.login_message = 'You need to be signed in to view this page.'
bcrypt = Bcrypt()
csrf = SeaSurf()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    register_blueprints(app)

    # Initialize Flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app


### Helper Functions ###
def register_blueprints(app):
    from minimart.pages import pages
    from minimart.auth import auth
    from minimart.products import products
    from minimart.categories import categories
    from minimart.dashboard import dashboard
    
    app.register_blueprint(pages)
    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(categories)
    app.register_blueprint(dashboard)

def initialize_extensions(app):
    from minimart.models import db
    from minimart.models import login_manager
    from minimart.models import mail
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

def configure_logging(app):
    # Deactivating the default Flask logger to prevent duplication of log messages
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('minimart.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)

def register_error_handlers(app):
    from flask import render_template

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html')

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html')

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404/html')

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('errors/405.html')

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html')
    

app = create_app()
app.app_context().push()
