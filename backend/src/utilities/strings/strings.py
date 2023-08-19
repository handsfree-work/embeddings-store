import random
import string


def generate_random_number_string(length):
    numbers = string.digits
    return ''.join(random.choice(numbers) for _ in range(length))
