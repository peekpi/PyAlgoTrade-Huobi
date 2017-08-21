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
from Util import *
import HuobiService as hapi

import time
import datetime
import hmac
import hashlib
import requests
import threading

from pyalgotrade.utils import dt
from pyalgotrade.bitstamp import common

import logging
logging.getLogger("requests").setLevel(logging.ERROR)


def parse_datetime(ret):
    return dt.as_utc(ret)


class AccountBalance(object):
    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getUSDAvailable(self):
        return float(self.__jsonDict["usd_available"])

    def getBTCAvailable(self):
        return float(self.__jsonDict["btc_available"])


class Order(object):
    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getId(self):
        return int(self.__jsonDict["id"])

    def isBuy(self):
        return self.__jsonDict["type"] == 0

    def isSell(self):
        return self.__jsonDict["type"] == 1

    def getPrice(self):
        return float(self.__jsonDict["price"])

    def getAmount(self):
        return float(self.__jsonDict["amount"])

    def getDateTime(self):
        return parse_datetime(self.__jsonDict["datetime"])


class UserTransaction(object):
    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getBTC(self):
        return float(self.__jsonDict["btc"])

    def getBTCUSD(self):
        return float(self.__jsonDict["btc_usd"])

    def getDateTime(self):
        return parse_datetime(self.__jsonDict["datetime"])

    def getFee(self):
        return float(self.__jsonDict["fee"])

    def getId(self):
        return int(self.__jsonDict["id"])

    def getOrderId(self):
        return int(self.__jsonDict["order_id"])

    def getUSD(self):
        return float(self.__jsonDict["usd"])


class HTTPClient(object):
    COIN_BTC = 1
    COIN_LTC = 2
    USER_AGENT = "PyAlgoTrade"
    REQUEST_TIMEOUT = 30

    class UserTransactionType:
        MARKET_TRADE = 2

    def __init__(self):
        self.__id = 0;
        self.__orders = []
        self.__prevNonce = None
        self.__lock = threading.Lock()
        self.getAllOrders()

    def __ID(self):
        self.__id += 1
        return self.__id

    def _getNonce(self):
        ret = int(time.time())
        if ret == self.__prevNonce:
            ret += 1
        self.__prevNonce = ret
        return ret

    def getAccountBalance(self):
        url = "https://www.bitstamp.net/api/balance/"
        jsonResponse = self._post(url, {})
        return AccountBalance(jsonResponse)

    def getOpenOrders(self):
        url = "https://www.bitstamp.net/api/open_orders/"
        jsonResponse = self._post(url, {})
        return [Order(json_open_order) for json_open_order in jsonResponse]

    def cancelOrder(self, orderId):
        url = "https://www.bitstamp.net/api/cancel_order/"
        params = {"id": orderId}
        jsonResponse = self._post(url, params)
        if jsonResponse != True:
            raise Exception("Failed to cancel order")

    def buyLimit(self, limitPrice, quantity):
        # Rounding price to avoid 'Ensure that there are no more than 2 decimal places'
        # error.
        price = round(limitPrice, 2)
        # Rounding amount to avoid 'Ensure that there are no more than 8 decimal places'
        # error.
        amount = round(quantity, 8)
        ret = hapi.buy(COIN_BTC, str(price), str(amount), None, None, BUY)
        if ret['result'] != 'success':
            return None
        self.__orders.append(ret['id'])
        dic={'id':ret['id'], 'type':0, 'price':price, 'amount':amount, 'datetime':datetime.now()}
        return Order(dic)

    def sellLimit(self, limitPrice, quantity):
        # Rounding price to avoid 'Ensure that there are no more than 2 decimal places'
        # error.
        price = round(limitPrice, 2)
        # Rounding amount to avoid 'Ensure that there are no more than 8 decimal places'
        # error.
        amount = round(quantity, 8)
        ret = hapi.sell(COIN_BTC, str(price), str(amount), None, str(tradeid), SELL)
        if ret['result'] != 'success':
            return None
        self.__orders.append(ret['id'])
        dic={'id':ret['id'], 'type':1, 'price':price, 'amount':amount, 'datetime':datetime.now()}
        return Order(dic)

    def getUserTransactions(self, transactionType=None):
        l = []
        sid = self.__ID(),
        dt = datetime.now()
        for oid in self.__orders:
            ret = hapi.getOrderInfo(COIN_BTC, oid, ORDER_INFO)
            fee = float(ret['fee'])
            filled = float(ret['processed_amount'])
            avgPrice = float(ret['processed_price'])
            vot = float(ret['vot'])
            l.append(UserTransaction({
                "order_id"  :   oid,
                "id"        :   sid,
                "btc"       :   filled,
                "btc_usd"   :   avgPrice,
                "usd"       :   vot,
                "datetime"  :   dt,
                "fee"       :   fee,
            }))
        return l

    def getAllOrder(self):
        ret = hapi.getOrders(COIN_BTC, GET_ORDERS)
        for order in ret:
            self.__orders.append(order['id'])
            
