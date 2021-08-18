from flask import Blueprint

dashboard = Blueprint('dashboard', __name__ , static_folder='static', template_folder='templates/dashboard', url_prefix='/dashboard')

from minimart.dashboard import routes