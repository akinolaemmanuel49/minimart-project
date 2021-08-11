from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField

from wtforms.validators import Email, InputRequired, ValidationError

from minimart.models import Product, ProductReview, ProductImageSet