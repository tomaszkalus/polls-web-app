import random
from string import ascii_letters

def generate_unique_identifier(length):
    return "".join(
        random.choice(ascii_letters) for _ in range(length))
