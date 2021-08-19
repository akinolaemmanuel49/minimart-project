from flask import Blueprint

products = Blueprint('products', __name__, static_folder='static', template_folder='templates', url_prefix='/products')

from minimart.products import routes
