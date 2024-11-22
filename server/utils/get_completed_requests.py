from os import listdir
from os.path import isfile, join


def get_completed_requests():
    return map(lambda x: x.strip().split('.')[0].strip(),[f for f in listdir("../results/") if isfile(join("../results/", f))])


if __name__ == "__main__":
    get_completed_requests()
