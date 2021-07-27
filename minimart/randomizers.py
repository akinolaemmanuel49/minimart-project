from random import choice
from minimart.models import Product, ProductReview


def generateProductID():
    """This function generates a unique id for the product object.
    `param:None`
    `returns:generated_id`"""
    char_set = [chr(i) for i in range(33, 58)] + [chr(i)
                                                  for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

    generated_id = ''

    for i in range(32):
        generated_id += choice(char_set)

    product = Product().query.filter_by(id=generated_id).first()
    if product:
        return generateProductID()

    return generated_id


def generateProductReviewID():
    """This function generates a unique id for the product review object.
    `param:None`
    `returns:generated_id`"""
    char_set = [chr(i) for i in range(33, 58)] + [chr(i)
                                                  for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

    generated_id = ''

    for i in range(32):
        generated_id += choice(char_set)

    product_review = ProductReview().query.filter_by(id=generated_id).first()
    if product_review:
        return generateProductReviewID()

    return generated_id