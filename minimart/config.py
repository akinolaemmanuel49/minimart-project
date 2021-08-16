import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'minimart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') or True
    ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE') or 3
    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or 5120 * 5120
    UPLOAD_EXTENSIONS = os.environ.get('UPLOAD_EXTENSIONS') or ['.jpg', '.png', '.gif', '.jpeg']
