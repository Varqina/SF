import time
import datetime


def convert_data_to_unix(date_as_string):
    if len(date_as_string) <= 10:
        return int(time.mktime(datetime.datetime.strptime(date_as_string, "%d/%m/%Y").timetuple()))
    else:
        return int(time.mktime(datetime.datetime.strptime(date_as_string, "%d/%m/%Y %H:%M:%S").timetuple()))
