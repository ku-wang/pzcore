import os
from decorator_module import retry


@retry.retry(3, 5)
def read_l(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip())
    return lines


def read_line(filename='test1'):
    if os.path.exists(filename):
        print("The {file} has existed ...")
        results = read_l(filename)
    else:
        print("The {file} not exist, will create it first ...")
        f = open(filename, "w")
        f.write("write something to file")
        f.close()
        results = read_l(filename)

    return results


read_l('ssss')

