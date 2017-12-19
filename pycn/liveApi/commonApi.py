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

import urllib2
import json

import time
import datetime

from hbsdk import ApiClient, ApiError

client = ApiClient('API_KEY', 'API_SECRET')

def getKLineBar(identifier, endTimestamp, period, length = 1):
    print('-------getKLine:%s %s %s %s'%(identifier, endTimestamp, period, length))
    length = length + 1 if length < 2000 else 2000

    klines = client.mget('/market/history/kline', symbol=identifier, period='%dmin'%period, size=length)
    print(len(klines))
    print(klines[0])
    print(klines[1])
    time.sleep(1)
    if len(kline) != size:
        return None
    del klines[0]
    x = klines[0]
    if x.id < endTimestamp:
        return None
    if x.id > endTimestamp:
        print('recv:%d expect:%d'%(x.id, endTimestamp))
        exit()

    return [ {
              "Timestamp":k.id,
              "Open":k.open,
              "High":k.high,
              "Low":k.low,
              "Close":k.close,
              "Volume":k.vol,
      }
      for k in klines
    ]

