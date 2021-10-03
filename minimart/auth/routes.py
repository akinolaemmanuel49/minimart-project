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
# def signup(email="", username="", error_message="", password_is_invalid="false", confirm_password_is_invalid="false", username_is_invalid="false", email_is_invalid="false"):
    title = 'Minimart - Signup'
    year = datetime.utcnow().year

    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = User(email=email, username=username)
        if User.query.filter_by(email=user.email).first():
            # email_is_invalid, error_message = "true", "This email address is already in use."
            # return redirect(url_for('auth.signup', email_is_invalid=email_is_invalid, error_message=error_message))
            return redirect(url_for('auth.signup'))
        if User.query.filter_by(username=user.username).first():
            print(User.query.filter_by(username=user.username).first())
            # username_is_invalid, error_message = "true", "This username has already in user, please choose another."
            # return redirect(url_for('auth.signup', username_is_invalid=username_is_invalid, error_message=error_message))
            return redirect(url_for('auth.signup'))
        if len(password) < 8:
            # password_is_invalid, error_message = "true", "Password must have atleast 8 characters."
            # return redirect(url_for('auth.signup', email=email, username=username, password_is_invalid=password_is_invalid, error_message=error_message))
            return redirect(url_for('auth.signup'))
        if len(password) > 32:
            # password_is_invalid, error_message = "true", "Password cannot exceed 32 characters."
            # return redirect(url_for('auth.signup', email=email, username=username, password_is_invalid=password_is_invalid, error_message=error_message))
            return redirect(url_for('auth.signup'))
        if password == confirm_password:
            user.set_password(password)
        else:
            # confirm_password_is_invalid, error_message = "true" ,"Passwords do not match."
            # return redirect(url_for('auth.signup', email=email, username=username, confirm_password_is_invalid=confirm_password_is_invalid, error_message=error_message))
            return redirect(url_for('auth.signup'))

        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed up', 'message')
        return redirect(url_for('auth.signin', email=email))
    return render_template('auth/signup.html', title=title, year=year)


@csrf.include
@auth.route('/signin', methods=['GET', 'POST'])
def signin(email=""):
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
    return render_template('auth/signin.html', title=title, year=year, email=email)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect (url_for('pages.home'))