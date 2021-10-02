import threading
import time

threadLock = threading.Lock()


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = round(time.time() * 1000)
        func(*args, **kwargs)
        print(f"{round(time.time() * 1000) - start_time} ms")
        return func(*args, **kwargs)

    return wrapper


def thread_lock(func):
    def wrapper(*args, **kwargs):
        threadLock.acquire()
        func(*args, **kwargs)
        threadLock.release()
        return func(*args, **kwargs)

    return wrapper
