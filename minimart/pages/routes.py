from datetime import datetime

from flask import render_template, url_for, request, current_app
from flask_login import current_user, AnonymousUserMixin

from minimart.pages import pages
from minimart.models import Product, Category

def get_category(id):
    category = Category.query.filter_by(id=id).first()
    return category

@pages.route('/', methods=['GET'])
@pages.route('/home', methods=['GET'])
@pages.route('/index', methods=['GET'])
def home():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created.desc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], True)
    next_view = url_for('pages.home', page=products.next_num) if products.has_next else None
    prev_view = url_for('pages.home', page=products.prev_num) if products.has_prev else None
    return render_template('pages/home.html', title=title, year=year, products=products.items, next_view=next_view, prev_view=prev_view, get_category=get_category)


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
