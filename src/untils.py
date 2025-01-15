import datetime
import random


def get_random_datetime(min_year=2023):
    dtMax = datetime.datetime.now()
    max_year = int(dtMax.strftime("%Y"))

    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    dt = start + (end - start) * random.random()
    return dt


def format_datetime_diff(diff):
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days} 日前"
    elif hours > 0:
        return f"{hours} 時間前"
    elif minutes > 0:
        return f"{minutes} 分前"
    else:
        return f"{seconds} 秒前"
