import random
import string
import time
import uuid


def generate_random_int(max_size, min_size=3):
    try:
        return random.randint(min_size, max_size)
    except Exception as e:
        print("Not supporting {0} as valid sizes!".format(max_size))
        raise e


def generate_random_string(max_size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(generate_random_int(max_size)))


def generate_doc():

    doc = {
        "doc_c_time": int(time.time() * 1000),
        "cc_id": str(uuid.uuid4()),
        "cc_name": generate_random_string(15),
        "tenant": generate_random_string(5),
        "name": '{0}.{1}'.format(generate_random_string(10), generate_random_string(3)),
        "name_term": '{0}.{1}'.format(generate_random_string(10), generate_random_string(3)),
        "is_file": True,
        "path": random.choice(["", "/", "/dir", "/dir" + "{}".format(random.randint(1, 100))]),
        "last_used_time": int(time.time() * 1000),
        'file_system': generate_random_string(5),
        "atime": int(time.time() * 1000),
        "mtime": int(time.time() * 1000),
        "ctime": int(time.time() * 1000),
        "size": random.randint(1, 1000000),
        "is_folder": False,
        "app_type": "Vizion Index & Search",
        "uid": random.randint(0,10),
        "denied": [],
        "app_id": str(uuid.uuid4()),
        "app_name": generate_random_string(10),
        "gid": random.randint(0, 10),
        "doc_i_time": int(time.time() * 1000),
        "file_id": str(random.randint(11111111111111111111111111111111, 99999911111111111111111111111111)),
        "file": generate_random_string(20),
        "allowed": ["FULL"]
    }

    return doc


def handle_docs(doc_nums):

        def split_list(lists, seg_length):
            inlist = lists[:]
            outlist = []

            while inlist:
                outlist.append(inlist[0:seg_length])
                inlist[0:seg_length] = []
            return outlist

        templates = []
        for num in range(1, doc_nums + 1):
            templates.append(generate_doc())

        return split_list(templates, 1000)


if __name__ == '__main__':
    c = handle_docs(1001)
    # print(c)
    print(len(c))