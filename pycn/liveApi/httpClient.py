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
#from pyalgotrade.Util import *
from commonTrade import tradeApi

from datetime import *

from pyalgotrade.utils import dt

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
                continue
    return forever

def str2datetime(s):
    return datetime.fromtimestamp(int(s))
#    return datetime.strptime(s,"%Y%m%d%H%M%S")

def parse_datetime(ret):
    return dt.as_utc(ret)


class AccountBalance(object):
    def __init__(self, jsonDict, instrument):
        self.__jsonDict = jsonDict
        self.__instrument = instrument

    def getUSDAvailable(self):
        return float(self.__jsonDict["available_money"])

    def getBTCAvailable(self):
        return float(self.__jsonDict["available_coin"])


class Order(object):
    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getId(self):
        return int(self.__jsonDict['id'])

    def isBuy(self):
        return self.__jsonDict["type"] == 1

    def isSell(self):
        return self.__jsonDict["type"] == 2

    def getPrice(self):
        return float(self.__jsonDict["order_price"])

    def getAmount(self):
        return float(self.__jsonDict["order_amount"])

    def getDateTime(self):
        return parse_datetime(str2datetime(self.__jsonDict["order_time"]))


class UserTransaction(object):
    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict
        self.__datetime = datetime.utcnow()

    def getBTC(self):
        return float(self.__jsonDict["processed_amount"])

    def getBTCUSD(self):
        return float(self.__jsonDict["processed_price"])

    def getDateTime(self):
        return self.__datetime

    def getFee(self):
        return float(self.__jsonDict["fee"])

    def getOrderId(self):
        return int(self.__jsonDict["id"])

    def getUSD(self):
        return float(self.__jsonDict["vot"])

    def isFilled(self):
        return self.__jsonDict["status"] == 2

    def isParityFilled(self):
        return self.__jsonDict["status"] == 1
        


class HuobiClient(object):
    def __init__(self, instrument):
        self.__instrument = instrument
        self.__coin = instrument

        if self.__coin is None:
            raise Exception("instrument is None")
        print('coin:%s'%self.__coin)
        self.__api = tradeApi()

    @tryForever
    def getAccountBalance(self):
        return self.__api.getAccountInfo()

    @tryForever
    def getOpenOrders(self):
        return self.__api.getOrders(self.__coin)
        
    def cancelOrder(self, orderId):
        print("cancelOrder:%s"%orderId)
        ret = self.__api.cancelOrder(self.__coin, orderId)
        if ret['result'] != "success":
            raise Exception("Failed to cancel order")

    def buyLimit(self, limitPrice, quantity):
        price = round(limitPrice, 2)
        amount = round(quantity, 4)
        return self.__api.buyLimit(self.__coin, str(price), str(amount), None, None, BUY)

    def sellLimit(self, limitPrice, quantity):
        price = round(limitPrice, 2)
        amount = round(quantity, 4)
        return self.__api.sellLimit(self.__coin, str(price), str(amount), None, str(tradeid), SELL)

    def getUserTransactions(self, ordersId):
        return [self.__api.getOrderInfo(self.__coin, oid) for oid in ordersId]

