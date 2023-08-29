import random
import string


def random_number_string(length):
    numbers = string.digits
    return ''.join(random.choice(numbers) for _ in range(length))


def sha256(text):
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def md5(text):
    import hashlib
    return hashlib.md5(text.encode('utf-8')).hexdigest()
