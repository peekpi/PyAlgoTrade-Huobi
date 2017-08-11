# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import urlparse
import urllib
import urllib2
import json
import pytz

from pyalgotrade.utils import dt


USE_SECURE_REQUESTS = False

# The exchange list comes from:
#  https://www.xignite.com/product/global-real-time-stock-quote-data/api/ListExchanges/
#
# I couldn't deduce the timezones for OOTC, PINX and XOTC using:
#  https://www.xignite.com/product/XigniteGlobalExchanges/api/GetExchangeHoursUTC/
#  https://www.xignite.com/product/XigniteGlobalExchanges/api/GetExchangeHours/

MARKET_TIMEZONES = {
    "ARCX": pytz.timezone("US/Eastern"),     # NYSE ARCA
    "CHIX": pytz.timezone("Europe/London"),  # CHI-X EUROPE LIMITED
    "XASE": pytz.timezone("US/Eastern"),     # NYSE MKT EQUITIES
    "XNAS": pytz.timezone("US/Eastern"),     # NASDAQ
    "XNYS": pytz.timezone("US/Eastern"),     # NEW YORK STOCK EXCHANGE, INC
}


class XigniteError(Exception):
    def __init__(self, message, response):
        Exception.__init__(self, message)
        self.__response = response

    def getResponse(self):
        return self.__response


def to_market_datetime(dateTime, exchange):
    timezone = MARKET_TIMEZONES.get(exchange)
    if timezone is None:
        raise Exception("No timezone available to localize datetime for exchange %s" % (exchange))
    return dt.localize(dateTime, timezone)


def datetime_to_string(dateTime, exchange):
    # MM/DD/YYYY HH:MM
    return to_market_datetime(dateTime, exchange).strftime("%m/%d/%Y %H:%M")


def json_http_request(url):
    f = urllib2.urlopen(url)
    response = f.read()
    print("resp:%s"%response)
    return json.loads(response)


def parse_instrument_exchange(identifier):
    ret = identifier.split(".")
    if len(ret) != 2:
        raise Exception("Invalid identifier. Exchange suffix is missing")
    return ret


def XigniteGlobalRealTime_GetBar(identifier, endDateTime, period, length = 1):
    if dt.datetime_is_naive(endDateTime):
        raise Exception("endDateTime must have a timezone")

    url = "http://api.huobi.com/staticmarket/ltc_kline_001_json.js?length=%d&timestamp=%s"%(length,endDateTime.strftime("%Y%m%d%H%M%S"))
    dic = json_http_request(url)[0]
#    "Date","Open","High","Low","Close","Volume","Adj Close"
    ret = {
            "Bar":{
              "Time":dic[0],
              "Open":dic[1],
              "High":dic[2],
              "Low":dic[3],
              "Close":dic[4],
              "Volume":dic[5],
            }
          }
    return ret
