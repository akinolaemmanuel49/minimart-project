from datetime import datetime

from minimart import db

# from minimart.randomizers import generateProductID, generateProductReviewID
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship('Profile', back_populates='user', uselist=False)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(128), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='profile')


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
    description = db.Column(db.Text(), nullable=True)
    header_image = db.Column(db.String(128),
                             nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='products')
    images = db.relationship(
        'ProductImageSet', backref='product', lazy='dynamic')
    reviews = db.relationship(
        'ProductReview', backref='product', lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def __init__(self, name, description):
    #     """
    #     Constructor method to initialize the model with a `name` and a `description`.
    #     """
    #     self.name = name
    #     self.description = description
    #     self.created = datetime.utcnow()
    #     self.modified = datetime.utcnow()

    def __repr__(self):
        """
        Returns a string representation of a `Product` object.
        """
        return 'Product<{}, {}>'.format(self.id, self.name)


class ProductImageSet(db.Model):
    """
    Class `ProductImageSet` inherits from the `flask_sqlalchemy` class `Model`.
    :param `id`: Provides a primary key for the `ProductImageSet` object.
    :param `url`: Provides a url for the image.
    :param `product_id`: Provides a foreign key reference to an object of the class `Product`.
    """

    __tablename__ = 'product_image_set'

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


class Category(db.Model):
    """
    Class `Category` inherits from the `flask_sqlalchemy` class `Model`.
    :param `id`: Provides a primary key for the `Category` object.
    :param `name`: Provides a name for `Category`.
    :param `product_id`: Provides a many to one relationship with the `Product` class.
    """

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return 'Category<{}, {}>'.format(self.id, self.name)
# class User(db.Model):
#     pass
