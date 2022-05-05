import time
import datetime
from calendar import monthrange

def convert_data_to_unix(date):
    if type(date) is int:
        return date
    if len(str(date)) <= 10:
        return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
    else:
        return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S").timetuple()))


def convert_unix_to_data(unix_data):
    if type(unix_data) is not int:
        return unix_data
    return datetime.datetime.utcfromtimestamp(unix_data).strftime("%Y/%m/%d %H:%M:%S")


def is_comparable_with_current_time(time_value, resolution):
    compared_value = int(time.time()) - time_value
    current_time = convert_unix_to_data(int(time.time()))
    if resolution == '1':
        return True if compared_value < 1*60 else False
    elif resolution == '5':
        return True if compared_value < 5*60 else False
    elif resolution == '15':
        return True if compared_value < 15*60 else False
    elif resolution == '30':
        return True if compared_value < 30*60 else False
    elif resolution == '60':
        return True if compared_value < 60*60 else False
    elif resolution == 'D':
        return True if compared_value < 24*60*60 else False
    elif resolution == 'W':
        return True if compared_value < 7*24*60*60 else False
    elif resolution == 'M':
        num_days = int(monthrange(int(current_time[:4]), int(current_time[5:7]))[1])
        return True if compared_value < num_days*7*24*60*60 else False
