from just.json_ import append
import time

START = "_".join(time.asctime().split())

LOG_FILE = "logs/{}_{}".format(__file__, START)


def log(obj, *tags):
    append({"tags": tags, "object": obj}, LOG_FILE)
