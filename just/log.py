import time
from just.json_ import append
import sys

START = "_".join(time.asctime().split())

LOG_FILE = "logs/{}_{}".format(sys.argv[0].rstrip(".py"), START)


def log(obj, *tags):
    append({"tags": tags, "object": obj}, LOG_FILE)
