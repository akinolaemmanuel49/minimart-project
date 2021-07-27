from flask import render_template
from minimart.products import products

from minimart.models import Product

@products.route('/list')
def product_list():
    title = 'Products'
    products = Product.query.all()
    return render_template('products_list.html', products=products)