import time

from data_requests.TimeManager import convert_unix_to_data


def add_b(func):
    def wrapper():
        func()
        print('b')
        return func()
    return wrapper

@add_b
def test():
    print('a')
    return True


a = convert_unix_to_data(int(time.time()))
print(a)
print(a[:7])