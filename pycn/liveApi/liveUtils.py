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

def priceRound(price):
    return round(price, 2)

def priceCoin(coin):
    return round(coin, 4)

import time
def tryForever(func):
    def forever(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception, e:
                print('')
                print('')
                print(' Exception: %s => %s'%(func.__name__, e.message)) 
                print('')
                print('')
                time.sleep(5)
                continue
    return forever

_eDict = {}
def exceDebug(fn):
    _eDict[fn] = True
    def waper(*args, **kwargs):
        __a = _eDict[fn]
        _eDict[fn] = not __a
        if __a is True:
            raise Exception('Debug:%s'%fn.__name__)
        print('')
        print('')
        print('==========success :: %s'%fn.__name__)
        print('')
        print('')
        return fn(*args, **kwargs)
    return waper

