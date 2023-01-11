from datetime import timedelta
from datetime import datetime


FORMAT = "%Y-%m-%d %H:%M:%S" 


def normalize(delta):
    if isinstance(delta, str):
        delta = delta.split(".")[0]
        delta = datetime.strptime(delta, FORMAT)
        delta = delta + timedelta(seconds = 1)
    return delta


def encode(delta):
    if isinstance(delta, str): return delta
    return datetime.strftime(delta, FORMAT)
