import time
import sys
import just

START = "_".join(time.asctime().replace(":", "_").split())

LOG_FILE = "logs/{}_{}.jsonl".format(sys.argv[0].rstrip(".py"), START)


def log(obj, *tags):
    just.append({"tags": tags, "object": obj}, LOG_FILE)
