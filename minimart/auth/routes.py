from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user
from minimart import db, login_manager
from minimart.auth import auth
from minimart.models import User
from sqlalchemy import exc


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
        if password == confirm_password:
            try:
                user = User(email=email, username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
            except exc.SQLAlchemyError:
                return flash('An error occurred. Try again', 'error')
    return render_template('auth/signup.html', title=title, year=year)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    title = 'Minimart - Signin'
    year = datetime.utcnow
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    if request.method is 'POST':
        user = User.filter_by(email=request.form.get('email')).first()
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
