from pyalgotrade.utils import dt
from datetime import datetime
import time
import pytz
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

localTz = pytz.timezone('Asia/Shanghai')

def timestamp():
    return int(time.time())

def utcnow():
    return dt.as_utc(datetime.utcnow())

def timestamp_to_DateTimeLocal(timestamp):
    return datetime.fromtimestamp(timestamp, localTz)

def utcToLocal(utcDatetime):
    return timestamp_to_DateTimeLocal(dt.datetime_to_timestamp(utcDatetime))

def PriceRound(price):
    return round(price, 2)

def CoinRound(coin):
    return round(coin, 4)

def ErrorShow(msg):
    __len = len(msg)
    if __len > 100:
        __len = 100
    print('--'*__len)
    print('-')
    print(msg.encode('utf8'))
    print('-')
    print('--'*__len)

import traceback

def tryForever(func):
    def forever(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception, e:
                print('----------traceback.print_exc:')
                traceback.print_exc()
                ErrorShow('Exception: %s => %s'%(func.__name__, e.message))
                time.sleep(1)
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

