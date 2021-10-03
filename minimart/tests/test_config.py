import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def test_development_config(app):
    app.config.from_object('minimart.config.DevelopmentConfig')
    assert app.config['FLASK_DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'minimart.db')

def test_testing_config(app):
    app.config.from_object('minimart.config.TestingConfig')
    assert app.config['FLASK_DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'minimart.db')

def test_production_config(app):
    app.config.from_object('minimart.config.ProductionConfig')
    assert not app.config['FLASK_DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'minimart.db')