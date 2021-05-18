import time
from functools import wraps


def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        print(f"{func.__name__} start")
        result = func(*args, **kargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__} end with {elapsed_time} seconds")
        return result

    return wrapper
