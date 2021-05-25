from datetime import datetime
from pytz import timezone


def now_with_timezone(tz: timezone) -> datetime:
    return datetime.now().astimezone().astimezone(tz)
