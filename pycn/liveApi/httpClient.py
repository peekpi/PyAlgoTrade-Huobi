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
    def __init__(self, jsonDict, vid):
        self.__jsonDict = jsonDict
        self.__vid = vid
        self.__datetime = datetime.now()

    def getBTC(self):
        return float(self.__jsonDict["processed_amount"])

    def getBTCUSD(self):
        return float(self.__jsonDict["processed_price"])

    def getDateTime(self):
        return parse_datetime(self.__datetime)

    def getFee(self):
        return float(self.__jsonDict["fee"])

    def getId(self):
        return int(self.__vid)

    def getOrderId(self):
        return int(self.__jsonDict["id"])

    def getUSD(self):
        return float(self.__jsonDict["vot"])

    def isFilled(self):
        return self.__jsonDict["status"] == 2

    def isParityFilled(self):
        return self.__jsonDict["status"] == 1
        


class HuobiClient(object):
    USER_AGENT = "PyAlgoTrade"
    REQUEST_TIMEOUT = 30

    class UserTransactionType:
        MARKET_TRADE = 2

    def __init__(self, instrument):
        self.__instrument = instrument
        self.__coin = instrument

        if self.__coin is None:
            raise Exception("instrument is None")
        print('coin:%s'%self.__coin)
        self.__api = tradeApi()
        self.__id = 0;
        self.__orders = []

    def __ID(self):
        self.__id += 1
        return self.__id

    @tryForever
    def getAccountBalance(self):
        ret = self.__api.getAccountInfo()
        return AccountBalance(ret, self.__instrument)

    @tryForever
    def getOpenOrders(self):
        ret = self.__api.getOrders(self.__coin)
        self.__orders = [d['id'] for d in ret]
        return [Order(d) for d in ret]
        
    def cancelOrder(self, orderId):
        print("cancelOrder:%s"%orderId)
        self.__orders.remove(orderId)
        return
        ret = self.__api.cancelOrder(self.__coin, orderId, CANCEL_ORDER)
        if ret['result'] != "success":
            raise Exception("Failed to cancel order")

    def buyLimit(self, limitPrice, quantity):
        price = round(limitPrice, 2)
        amount = round(quantity, 4)
        ret = {'id':self.__ID()}
        '''
        ret = self.__api.buyLimit(self.__coin, str(price), str(amount), None, None, BUY)
        if ret['result'] != 'success':
            return None
        '''
        self.__orders.append(ret['id'])
        dic={'id':ret['id'], 'type':1, 'order_price':price, 'order_amount':amount, 'order_time':time.time()}
        print("<<buyLimit:%s"%dic)
        return Order(dic)

    def sellLimit(self, limitPrice, quantity):
        price = round(limitPrice, 2)
        amount = round(quantity, 4)
        ret = {'id':self.__ID()}
        '''
        ret = self.__api.sellLimit(self.__coin, str(price), str(amount), None, str(tradeid), SELL)
        if ret['result'] != 'success':
            return None
        '''
        self.__orders.append(ret['id'])
        dic={'id':ret['id'], 'type':2, 'order_price':price, 'order_amount':amount, 'order_time':time.time()}
        print(">>sellLimit:%s"%dic)
        return Order(dic)

    def getUserTransactions(self, transactionType=None):
        l = []
        sid = self.__ID()
        dt = datetime.utcnow()
        for oid in self.__orders:
            #ret = self.__api.getOrderInfo(self.__coin, oid, ORDER_INFO)
            ret = {'status': 2, 'fee': '0.002', 'order_amount': '1', 'vot': '0.00', 'order_price': '23902.73', 'id': oid, 'total': '0.00', 'type': 1, 'processed_price': '23902.73', 'processed_amount': '0.998'}
            if ret.get('id') is not None:
                trans = UserTransaction(ret, sid)
                if trans.isFilled():
                    self.__orders.remove(oid)
                l.append(trans)
        return l

