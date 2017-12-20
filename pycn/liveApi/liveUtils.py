from pyalgotrade.utils import dt
from datetime import datetime
import pytz

localTz = pytz.timezone('Asia/Shanghai')

def utcnow():
    return dt.as_utc(datetime.utcnow())

def timestamp_to_DateTimeLocal(timestamp):
    return datetime.fromtimestamp(timestamp, localTz)

def utcToLocal(utcDatetime):
    return timestamp_to_DateTimeLocal(dt.datetime_to_timestamp(utcDatetime))

