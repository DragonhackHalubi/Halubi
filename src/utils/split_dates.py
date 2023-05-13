import pandas
from datetime import date, timedelta, datetime

def split_dates(date_string: str):
    start = date_string.split("-")[0]
    end = date_string.split("-")[1]

    start = date(2000, int(start.split(".")[1]), int(start.split(".")[0]))
    end = date(2000, int(end.split(".")[1]), int(end.split(".")[0])) + timedelta(days=1)

    dates_range = pandas.date_range(start,end-timedelta(days=1),freq='d').to_list()

    dates = [f"{single_date.strftime('%#d')}.{single_date.strftime('%#m')}." for single_date in dates_range]

    return dates
