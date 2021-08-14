from datetime import datetime

from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user

from minimart import db, login_manager
from minimart.auth import auth

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Minimart - Signup'
    year = datetime.utcnow().year
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

