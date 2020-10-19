import random
import string


def generate_random_int(max_size, min_size=3):
    try:
        return random.randint(min_size, max_size)
    except Exception as e:
        print("Not supporting {0} as valid sizes!".format(max_size))
        raise e


def generate_random_string(max_size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(generate_random_int(max_size)))


if __name__ == '__main__':
    print(generate_random_string(12))