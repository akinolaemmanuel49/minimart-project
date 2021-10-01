from datetime import datetime

from flask import current_app as minimart
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from flask_login.utils import logout_user
from minimart import csrf
from minimart.auth import auth
from minimart.models import db, User
from sqlalchemy import exc
from werkzeug.urls import url_parse


@csrf.include
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Minimart - Signup'
    year = datetime.utcnow().year
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        print(password)
        confirm_password = request.form.get('confirm_password')
        print(confirm_password)
        if len(password) < 8:
            flash('Password must have atleast 8 characters.', 'error')
            return redirect(url_for('auth.signup'))
        if len(password) > 32:
            flash('Password cannot exceed 32 characters.', 'error')
            return redirect(url_for('auth.signup'))
        if password == confirm_password:
            verified_password = password
        else:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.signup'))
        user = User(email=email, username=username)
        user.set_password(verified_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up', 'message')
        return redirect(url_for('auth.signin'))
    return render_template('auth/signup.html', title=title, year=year)


@csrf.include
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    title = 'Minimart - Signin'
    year = datetime.utcnow().year
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None:
            flash('Invalid email address')
            return redirect(url_for('auth.signin'))
        if user.check_password(request.form.get('password')):
            login_user(user, remember=request.form.get('remember_me'))
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('pages.home')
            return redirect(next_page)
    return render_template('auth/signin.html', title=title, year=year)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect (url_for('pages.get_current_user'))