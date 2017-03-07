import time
import sys
import just
import os

START = "_".join(time.asctime().replace(":", "_").split())
NAME = sys.argv[0].rstrip(".py")
LOG_BASE = "logs"
LOG_FILE = "{}/{}_{}.jsonl".format(LOG_BASE, NAME, START)
LOG_LINK = "{}/{}.jsonl".format(LOG_BASE, NAME)


def log(obj, *tags):
    just.append({"tags": tags, "object": obj}, LOG_FILE)
