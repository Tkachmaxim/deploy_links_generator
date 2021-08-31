import random
import string


def get_short_code():
    length = 6
    char = string.digits + string.ascii_uppercase + string.ascii_lowercase
    return ''.join(random.choice(char) for x in range(length))
