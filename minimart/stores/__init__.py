from flask import Blueprint

dashboard = Blueprint('stores', __name__ , static_folder='static', template_folder='templates')

from minimart.stores import routes