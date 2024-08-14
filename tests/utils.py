import random
import string


def get_random_string() -> str:
    length = random.randint(1, 200)
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))
