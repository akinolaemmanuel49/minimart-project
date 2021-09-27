import os
from datetime import datetime

from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from minimart import csrf
from minimart.models import Category, Product, db
from minimart.products import products
from sqlalchemy import exc


def get_category(id):
    category = Category.query.filter_by(id=id).first()
    return category


@products.route('/categories', methods=['GET'])
@products.route('/categories/explore', methods=['GET'])
def categories_list():
    title = 'Minimart - Categories'
    year = datetime.utcnow().year
    categories = Category.query.all()
    return render_template('products/categories_list.html', title=title, year=year, categories=categories)


@products.route('/category/<category_name>', methods=['GET'])
@products.route('/category/<category_name>/explore', methods=['GET'])
def category_explore(category_name):
    title = 'Minimart - {}'.format(category_name)
    year = datetime.utcnow().year
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(name=category_name).first()
    products = Product.query.filter_by(category=category.id).order_by(
        Product.created.desc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], True)
    next_view = url_for('products.category_explore', category_name=category_name,
                        page=products.next_num) if products.has_next else None
    prev_view = url_for('products.category_explore', category_name=category_name,
                        page=products.prev_num) if products.has_prev else None
    return render_template('products/explore_product_by_category.html', title=title, year=year, products=products.items, next_view=next_view, prev_view=prev_view, get_category=get_category)


@products.route('/explore', methods=['GET'])
def products_list():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created.desc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], True)
    next_view = url_for('products.products_list',
                        page=products.next_num) if products.has_next else None
    prev_view = url_for('products.products_list',
                        page=products.prev_num) if products.has_prev else None
    return render_template('products/products_list.html', title=title, year=year, products=products.items, next_view=next_view, prev_view=prev_view, get_category=get_category)


@products.route('/<int:product_id>', methods=['GET'])
def product_view(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    title = f'Minimart - {product.name}'
    year = datetime.utcnow().year
    return render_template('products/products_view.html', product=product, title=title, year=year, get_category=get_category)


@products.route('/product/<filename>', methods=['GET'])
def send_uploaded_image(filename):
    from flask import send_from_directory
    return send_from_directory(current_app.config['IMAGE_UPLOADS'], filename)


@csrf.include
@products.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    title = f'Minimart - Add product'
    year = datetime.utcnow().year
    categories = Category.query.all()
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_category = request.form.get('product_category')

        category = Category.query.filter_by(name=product_category).first()
        if category:
            product = Product(name=product_name)
            db.session.add(product)
            product.user_id = current_user.id
            product.category = category.id
            if request.files:
                from minimart.products.utils.string_generator import generate_string
                image = request.files["product_image"]
                image.filename = str(current_user.id) + "_" + generate_string(image.filename)
                img_path = os.path.join(
                    current_app.config['IMAGE_UPLOADS'], image.filename)
                image.save(img_path)
                print(f"IMAGE SAVED AT {img_path}")
            product.image = image.filename
            db.session.commit()
            return redirect(url_for('products.product_view', product_id=product.id))
    return render_template('products/create_product.html', title=title, year=year, categories=categories)


@csrf.include
@products.route('<int:id>/delete')
@login_required
def delete_product(id):
    if request.method == 'POST':
        product = Product.query.filter_by(id=id).first()
        if current_user.get_role() in ['admin', 'staff']:
            db.session.delete(product)
            db.session.commit()
        elif product.user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()
        else:
            return render_template('no_permission.html')
    return redirect(url_for('pages.home'))
