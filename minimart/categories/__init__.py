from flask import Blueprint

categories = Blueprint('categories', __name__, static_folder='static', template_folder='templates', url_prefix='/categories')

from minimart.categories import routes
