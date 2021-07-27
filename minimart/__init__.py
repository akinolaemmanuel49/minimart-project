# import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from minimart.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from minimart.models import db
    db.init_app(app)
    migrate.init_app(app, db, os.path.abspath(os.path.dirname(__file__)))

    # register blueprints.
    from minimart.products import products
    app.register_blueprint(products)

    return app


app = create_app()
app.app_context().push()

# print(os.path.abspath(os.path.dirname(__file__)))
