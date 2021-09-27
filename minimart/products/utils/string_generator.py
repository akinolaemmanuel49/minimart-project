import random
from datetime import datetime

def generate_string(seed_value=None):

    extension = str(seed_value.split('.')[-1])
    random.seed(seed_value + str(datetime.now()))

    STRING = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    generated_string = ""

    for i in range(10):
        generated_string += random.choice(STRING)
    return generated_string + '.' + extension
