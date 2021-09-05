import time
import datetime


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
    print(compared_value)
    candle_time_value = convert_unix_to_data(time_value)
    current_time = convert_unix_to_data(int(time.time()))
    if resolution is '1' or resolution is '5':
        return True if candle_time_value[:16] == current_time[:16] else False
    elif resolution is '15' or resolution is '30':
        return True if candle_time_value[:15] == current_time[:15] else False
    elif resolution is '60':
        return True if candle_time_value[:13] == current_time[:13] else False
    elif resolution is 'D' or resolution is 'W':
        return True if candle_time_value[:10] == current_time[:10] else False
    elif resolution is 'M':
        return True if candle_time_value[:7] == current_time[:7] else False
