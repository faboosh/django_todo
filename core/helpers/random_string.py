import string
import random

def random_string(num):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num))
