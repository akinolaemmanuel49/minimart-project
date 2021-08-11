from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from minimart.auth import auth


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))

