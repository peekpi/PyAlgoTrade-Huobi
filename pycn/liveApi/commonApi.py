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

MINSTR = {
    1:'001',
    5:'005',
    15:'015',
    30:'030',
    60:'060',
    60*24:'100',
}

def getKLineBar(identifier, endTimestamp, period, length = 1):
    length = length + 1 if length < 2000 else 2000
    url = "http://api.huobi.com/staticmarket/%s_kline_%s_json.js?length=%d&timestamp=%d"%(identifier, MINSTR[period], length, time.time())
    dics = json_http_request(url)
    dics.pop()
#    dic.sort(key=lambda x:x[0])
#    "Date","Open","High","Low","Close","Volume","Adj Close"
    if timeStr != dics[-1][0]:
        return None
    lastTime = timeStr
    return [ {
              "Time":dic[0],
              "Open":dic[1],
              "High":dic[2],
              "Low":dic[3],
              "Close":dic[4],
              "Volume":dic[5],
      }
      for dic in dics
    ]

