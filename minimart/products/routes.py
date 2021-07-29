from datetime import datetime

from flask import render_template
from minimart.models import Product
from minimart.products import products


@products.route('/explore')
def product_list():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    products = Product.query.all()
    return render_template('products/products_list.html', title=title, year=year, products=products)


@products.route('/<int:product_id>')
def product_view(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    title = f'Minimart - {product.name}'
    year = datetime.utcnow().year
    return render_template('products/product_view.html', product=product, title=title, year=year)
