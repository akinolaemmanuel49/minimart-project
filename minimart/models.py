from datetime import datetime

from minimart import db

# from minimart.randomizers import generateProductID, generateProductReviewID


class Product(db.Model):
    """
    Class `Product` inheriting from flask_sqlalchemy's `Model` class.
    :param `id`: Provides a primary key for a `Product` object.
    :param `name`: Provides the name of the `Product` object.
    :param `description`: Provides a summary for the `Product` object.
    :param `header_image`: URL to the product's profile image.
    :param `images`: A one to many relationship providing URL's to images of the product.
    :param `created`: Tells when a Product object was created.
    :param `modified`: Tells when a Product object was last modified.
    """

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    category = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    header_image = db.Column(db.String(128),
                             nullable=True)
    images = db.relationship(
        'ProductImageSet', backref='product', lazy='dynamic')
    reviews = db.relationship(
        'ProductReview', backref='product', lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, description):
        """
        Constructor method to initialize the model with a `name` and a `description`.
        """
        self.name = name
        self.description = description

    def __repr__(self):
        """
        Returns a string representation of a `Product` object.
        """
        return f'Product({self.name}, {self.created}, {self.modified})'


class ProductImageSet(db.Model):
    """
    Class `ProductImageSet` inherits from the `flask_sqlalchemy` class `Model`.
    :param `id`: Provides a primary key for the `ProductImageSet` object.
    :param `url`: Provides a url for the image.
    :param `product_id`: Provides a foreign key reference to an object of the class `Product`.
    """

    __tablename__ = 'image_set'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class ProductReview(db.Model):
    """
    Class `ProductReview` inherits from the `flask_sqlalchemy` class `Model`.
    :param `id`: Provides a primary key for the `ProductReview` object.
    :param `rating`: Provides a rating for `ProductReview`.
    :param `review`: Provides a review for `ProductReview`.
    :param `product_id`: Provides a foreign key reference to an object of the class `Product`.
    """

    __tablename__ = 'product_review'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(5), nullable=True)
    review = db.Column(db.Text())
    # owner = NotImplemented
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


# class User(db.Model):
#     pass
