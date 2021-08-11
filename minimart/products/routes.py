from datetime import datetime

from flask import current_app, render_template, request, url_for, flash, redirect
from minimart import db
from minimart.models import Product, Category
from minimart.products import products
from sqlalchemy import exc


@products.route('/category/explore', methods=['GET'])
def category_list():
    title = 'Minimart - Categories'
    year = datetime.utcnow().year
    categories = Category.query.all()
    return render_template('products/categories_list.html', title=title, year=year, categories=categories)


@products.route('/explore', methods=['GET'])
def products_list():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created.desc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    next_view = url_for('products.products_list', page=products.next_num) if products.has_next else None
    prev_view = url_for('products.products_list', page=products.prev_num) if products.has_prev else None
    return render_template('products/products_list.html', title=title, year=year, products=products.items, next_view=next_view, prev_view=prev_view)


@products.route('/<int:product_id>', methods=['GET'])
def product_view(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    title = f'Minimart - {product.name}'
    year = datetime.utcnow().year
    return render_template('products/product_view.html', product=product, title=title, year=year)


@products.route('/add', methods=['GET', 'POST'])
def product_add():
    title = f'Minimart - Add product'
    year = datetime.utcnow().year
    categories = Category.query.all()
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_category = request.form.get('product_category')
    category = Category.query.filter_by(name=product_name)
    if category:
        try:
            product = Product(name=product_name, category=product_category)
            db.session.add(product)
            db.session.commit()
            redirect(url_for('products.product_profile', id=product.id))
        except exc.SQLAlchemyError:
            return flash('An error occurred try again', 'error')

    return render_template('products/add_product.html', title=title, year=year, categories=categories)


@products.route('/profile/<int:id>', methods=['GET', 'POST'])
def product_profile(id):
    return id
