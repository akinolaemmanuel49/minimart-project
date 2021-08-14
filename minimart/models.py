from datetime import datetime
import json

from flask_login import UserMixin

from minimart import db, bcrypt

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, blank=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, blank=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False, blank=False)
    role = db.Column(db.String(5), nullable=False, blank=False, default='user')
    token = db.Column(db.String(32), unique=True, index=True)
    token_expiration = db.Column(db.DateTime)
    products = db.relationship('Product', backref='vendor', lazy='dynamic')
    last_seen = db.Column(db.Datetime, default=datetime.utcnow)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password)

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    def set_role(self, role):
        if role in ['user', 'staff', 'admin']:
            self.role = role
        else:
            raise Exception('Invalid role.')

    def get_role(self):
        return self.role

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Cart(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', backref='cart_item', lazy='dynamic')


class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, blank=False)
    description = db.Column(db.Text(), nullable=True)
    category = db.relationship('Category', backref='categories', lazy='dynamic')
    reviews = db.relationship('ProductReview', backref='product_reviews', lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return 'Product<{}, {}, {}>'.format(self.id, self.category, self.name)


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, blank=False)

    def __repr__(self):
        return 'Category<{}>'.format(self.name)
