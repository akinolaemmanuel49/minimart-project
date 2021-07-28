from datetime import datetime

from flask import render_template
from minimart.models import Product
from minimart.products import products


@products.route('/list')
def product_list():
    title = 'Minimart - Products'
    year = datetime.utcnow().year
    products = Product.query.all()
    return render_template('products/products_list.html', title=title, products=products, year=year)

# @products.route('/<id>')