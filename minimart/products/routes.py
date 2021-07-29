from datetime import datetime

from flask import current_app, render_template, request, url_for
from minimart.models import Product
from minimart.products import products


@products.route('/explore', methods=['GET'])
def products_list():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created.desc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], True)
    next_view = url_for(
        'product_list', page=products.next_num) if products.has_next else None
    prev_view = url_for(
        'product_list', page=products.prev_num) if products.has_prev else None

    return render_template('products/products_list.html', title=title, year=year, products=products.items, next_view=next_view, prev_view=prev_view
                           )


@products.route('/<int:product_id>', methods=['GET'])
def product_view(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    title = f'Minimart - {product.name}'
    year = datetime.utcnow().year
    return render_template('products/product_view.html', product=product, title=title, year=year)
