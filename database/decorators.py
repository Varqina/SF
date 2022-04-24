""" Decorators for a project"""
import threading
import time

threadLock = threading.Lock()


def measure_time(func):
    """Decorator for measurement the execution time of any function"""
    def wrapper(*args, **kwargs):
        start_time = round(time.time() * 1000)
        func(*args, **kwargs)
        print(f"{round(time.time() * 1000) - start_time} ms")
    return wrapper


def thread_lock(func):
    """Decorator for thread lock"""
    def wrapper(*args, **kwargs):
        threadLock.acquire()
        func(*args, **kwargs)
        threadLock.release()
    return wrapper
