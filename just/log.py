import time
from just.json_ import append

START = "_".join(time.asctime().split())

LOG_FILE = "logs/{}_{}".format(__name__, START)


def log(obj, *tags):
    append({"tags": tags, "object": obj}, LOG_FILE)
