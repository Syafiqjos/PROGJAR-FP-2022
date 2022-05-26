import random
import string


def random_string(n):
    return "".join(random.choice(string.ascii_letters) for _ in range(n))
