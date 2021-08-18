from datetime import datetime

from flask import render_template
from flask_login import current_user, AnonymousUserMixin

from minimart.pages import pages

@pages.route('/', methods=['GET'])
@pages.route('/home', methods=['GET'])
@pages.route('/index', methods=['GET'])
def home():
    title = 'Minimart - Home'
    year = datetime.utcnow().year
    return render_template('pages/home.html', title=title, year=year)


@pages.route('/about-us', methods=['GET'])
def about_us():
    title = 'Minimart - About us'
    year = datetime.utcnow().year
    return render_template('pages/about-us.html', title=title, year=year)


@pages.route('/get_current_user', methods=['GET'])
def get_current_user():
    title = 'REMOVE LATER'
    year = datetime.utcnow().year
    user = current_user
    flag = False
    if isinstance(user, AnonymousUserMixin):
        flag = True
    return render_template('pages/get_current_user.html', title=title, year=year, user=user, flag=flag)
