from datetime import datetime

from flask import render_template, redirect, request, current_app
from flask_login import login_required
from werkzeug import routing

from minimart.stores import stores

@stores.route('store/register', method=['GET', 'POST'])
def store_register():
    title = 'Minimart - Register your store'
    year = datetime.utcnow().year

    if request.method == 'POST':
        
