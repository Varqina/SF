import time
import datetime


def convert_data_to_unix(date):
    if type(date) is int:
        return date
    if len(str(date)) <= 10:
        return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
    else:
        return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S").timetuple()))


def is_comparable_with_current_time(time_value):
    compared_value = int(time.time()) - time_value
    print(compared_value)
    return True if compared_value < 30 else False
