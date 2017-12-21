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
import datetime
from pyalgotrade.utils import dt

import abc

class TradeAccountBalanceBase(object):
    # return available cash, float .2
    @abc.abstractmethod
    def getUSDAvailable(self):
        raise NotImplementedError()

    # return available coin, float .4
    @abc.abstractmethod
    def getBTCAvailable(self):
        raise NotImplementedError()


class TradeOrderBase(object):
    def __init__(self):
        self.__datetime = dt.as_utc(datetime.datetime.utcnow())
    # return order ID, int
    @abc.abstractmethod
    def getId(self):
        raise NotImplementedError()

    # return buy or sell, boolean
    @abc.abstractmethod
    def isBuy(self):
        raise NotImplementedError()

    # return buy or sell, boolean
    @abc.abstractmethod
    def isSell(self):
        raise NotImplementedError()

    # return Price, float .2
    @abc.abstractmethod
    def getPrice(self):
        raise NotImplementedError()

    # return coin num, float .4
    @abc.abstractmethod
    def getAmount(self):
        raise NotImplementedError()

    # return order time, datetime.datetime
    def getDateTime(self):
        return self.__datetime


class TradeUserTransactionBase(object):
    def __init__(self):
        self.__datetime = dt.as_utc(datetime.datetime.utcnow())

    # return filled coin num, float .4
    @abc.abstractmethod
    def getBTC(self):
        raise NotImplementedError()

    # return avarage fillled price, float .2
    @abc.abstractmethod
    def getBTCUSD(self):
        raise NotImplementedError()

    # return fee, float .4
    @abc.abstractmethod
    def getFee(self):
        raise NotImplementedError()

    # return order ID, int
    @abc.abstractmethod
    def getOrderId(self):
        raise NotImplementedError()

    # return order is filled, boolean
    @abc.abstractmethod
    def isFilled(self):
        raise NotImplementedError()

    # return time, datetime.datetime
    def getDateTime(self):
        return self.__datetime


class TradeClientBase(object):
    def __init__(self, instrument):
        if instrument is None:
            raise Exception("instrument is None")
        self.__coin = instrument

    def getCoinType(self):
        return self.__coin

    # return class(AccountBalance)
    @abc.abstractmethod
    def getAccountBalance(self):
        raise NotImplementedError()

    # return [class(Order), ...]
    @abc.abstractmethod
    def getOpenOrders(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def cancelOrder(self, orderId):
        raise NotImplementedError()

    # return class(Order)
    @abc.abstractmethod
    def buyLimit(self, limitPrice, quantity):
        raise NotImplementedError()

    # return class(Order)
    @abc.abstractmethod
    def sellLimit(self, limitPrice, quantity):
        raise NotImplementedError()

    # return [class(UserTransaction), ...]
    @abc.abstractmethod
    def getUserTransactions(self, ordersId):
        raise NotImplementedError()

