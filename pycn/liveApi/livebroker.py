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

import threading
import time
import Queue

from pyalgotrade import broker
#import httpclient
from pyalgotrade.bitstamp import common
import liveUtils

def build_order_from_open_order(openOrder, instrumentTraits):
    if openOrder.isBuy():
        action = broker.Order.Action.BUY
    elif openOrder.isSell():
        action = broker.Order.Action.SELL
    else:
        raise Exception("Invalid order type")

    ret = broker.LimitOrder(action, common.btc_symbol, openOrder.getPrice(), openOrder.getAmount(), instrumentTraits)
    ret.setSubmitted(openOrder.getId(), openOrder.getDateTime())
    ret.setState(broker.Order.State.ACCEPTED)
    return ret

class TradeMonitor(threading.Thread):
    POLL_FREQUENCY = 2

    # Events
    ON_USER_TRADE = 1
    # Events Order
    ORDER_DEL = 1
    ORDER_ADD = 2

    def __init__(self, httpClient):
        super(TradeMonitor, self).__init__()
        self.__httpClient = httpClient
        self.__queue = Queue.Queue()
        self.__queueOrder = Queue.Queue()
        self.__ordersId = []
        self.__stop = False
        print("livebroker.TradeMonitor.__init__: POLL_FREQUENCY is %d"%TradeMonitor.POLL_FREQUENCY)
        print("common.btc_symbol:%s"%common.btc_symbol)

    def __wait(self):
        sleepTime = 0
        while not self.__stop and sleepTime < TradeMonitor.POLL_FREQUENCY:
            time.sleep(1)
            sleepTime += 1

    def __syncOrderId(self):
        try:
            while not self.__queueOrder.empty():
                event, oid = self.__queueOrder.get_nowait()
                if event == TradeMonitor.ORDER_ADD:
                    self.__ordersId.append(oid)
                else:
                    self.__ordersId.remove(oid)
        except:
            pass
    def addOrderIdSafety(self, oid):
        self.__queueOrder.put((TradeMonitor.ORDER_ADD, oid))
    def delOrderIdSafety(self, oid):
        self.__queueOrder.put((TradeMonitor.ORDER_DEL, oid))

    @liveUtils.tryForever
    def _getNewTrades(self):
        self.__syncOrderId()
        return self.__httpClient.getUserTransactions(self.__ordersId)

    def getQueue(self):
        return self.__queue

    def start(self):
        super(TradeMonitor, self).start()

    def run(self):
        while not self.__stop:
            try:
                trades = self._getNewTrades()
                if len(trades):
                    common.logger.info("%d new trade/s found" % (len(trades)))
                    self.__queue.put((TradeMonitor.ON_USER_TRADE, trades))
            except Exception, e:
                common.logger.critical("Error retrieving user transactions", exc_info=e)
            self.__wait()

    def stop(self):
        self.__stop = True


class LiveBroker(broker.Broker):
    """A Bitstamp live broker.

    :param clientId: Client id.
    :type clientId: string.
    :param key: API key.
    :type key: string.
    :param secret: API secret.
    :type secret: string.


    .. note::
        * Only limit orders are supported.
        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.
        * BUY_TO_COVER orders are mapped to BUY orders.
        * SELL_SHORT orders are mapped to SELL orders.
        * API access permissions should include:

          * Account balance
          * Open orders
          * Buy limit order
          * User transactions
          * Cancel order
          * Sell limit order
    """

    QUEUE_TIMEOUT = 0.01

    def __init__(self, instrument, TradeClient):
        super(LiveBroker, self).__init__()
        self.__symbol = instrument
        common.btc_symbol = instrument
        self.__stop = False
        self.__httpClient = TradeClient
        self.__tradeMonitor = TradeMonitor(self.__httpClient)
        self.__cash = 0
        self.__shares = {}
        self.__activeOrders = {}

    def _registerOrder(self, order):
        assert(order.getId() not in self.__activeOrders)
        assert(order.getId() is not None)
        self.__activeOrders[order.getId()] = order
        self.__tradeMonitor.addOrderIdSafety(order.getId())

    def _unregisterOrder(self, order):
        assert(order.getId() in self.__activeOrders)
        assert(order.getId() is not None)
        del self.__activeOrders[order.getId()]
        self.__tradeMonitor.delOrderIdSafety(order.getId())

    @liveUtils.tryForever
    def refreshAccountBalance(self):
        """Refreshes cash and BTC balance."""

        self.__stop = True  # Stop running in case of errors.
        common.logger.info("Retrieving account balance.")
        balance = self.__httpClient.getAccountBalance()

        # Cash
        self.__cash = round(balance.getUSDAvailable(), 2)
        common.logger.info("%s USD" % (self.__cash))
        # BTC
        btc = balance.getBTCAvailable()
        if btc:
            self.__shares = {common.btc_symbol: btc}
        else:
            self.__shares = {}
        common.logger.info("%s BTC" % (btc))

        self.__stop = False  # No errors. Keep running.

    @liveUtils.tryForever
    def refreshOpenOrders(self):
        self.__stop = True  # Stop running in case of errors.
        common.logger.info("Retrieving open orders.")
        openOrders = self.__httpClient.getOpenOrders()
        for openOrder in openOrders:
            self._registerOrder(build_order_from_open_order(openOrder, self.getInstrumentTraits(common.btc_symbol)))

        common.logger.info("%d open order/s found" % (len(openOrders)))
        self.__stop = False  # No errors. Keep running.

    def _startTradeMonitor(self):
        self.__stop = True  # Stop running in case of errors.
        common.logger.info("Initializing trade monitor.")
        self.__tradeMonitor.start()
        self.__stop = False  # No errors. Keep running.

    def _onUserTrades(self, trades):
        ret = False
        for trade in trades:
            order = self.__activeOrders.get(trade.getOrderId())
            if order is not None:
                filled = order.getFilled()
                avgPrice = order.getAvgFillPrice()
                newQuantity = trade.getBTC() - filled
                if newQuantity == 0:
                    continue
                ret = True
                newFillPrice = trade.getBTCUSD()
                if avgPrice is not None:
                    newFillPrice = (newFillPrice * trade.getBTC() - order.getFilled() * avgPrice)/newQuantity
                newFee = trade.getFee() - order.getCommissions()
                newDateTime = trade.getDateTime()

                print('--new: price:%f btc:%f fee:%s time:%s'%(newFillPrice, newQuantity, newFee, newDateTime))

                # Update cash and shares.
                self.refreshAccountBalance()
                # Update the order.
                orderExecutionInfo = broker.OrderExecutionInfo(newFillPrice, abs(newQuantity), newFee, newDateTime)
                order.addExecutionInfo(orderExecutionInfo)
                if trade.isFilled():
                    order.setState(order.State.FILLED)
#                order.updateExecutionInfo(orderExecutionInfo)
                if not order.isActive():
                    self._unregisterOrder(order)
                # Notify that the order was updated.
                if order.isFilled():
                    eventType = broker.OrderEvent.Type.FILLED
                else:
                    eventType = broker.OrderEvent.Type.PARTIALLY_FILLED
                self.notifyOrderEvent(broker.OrderEvent(order, eventType, orderExecutionInfo))
            else:
                common.logger.info("Trade refered to order %d that is not active" % (trade.getOrderId()))
        return ret

    # BEGIN observer.Subject interface
    def start(self):
        super(LiveBroker, self).start()
        self.refreshAccountBalance()
        self.refreshOpenOrders()
        self._startTradeMonitor()

    def stop(self):
        self.__stop = True
        common.logger.info("Shutting down trade monitor.")
        self.__tradeMonitor.stop()

    def join(self):
        if self.__tradeMonitor.isAlive():
            self.__tradeMonitor.join()

    def eof(self):
        return self.__stop

    def dispatch(self):
        # Switch orders from SUBMITTED to ACCEPTED.
        ordersToProcess = self.__activeOrders.values()
        for order in ordersToProcess:
            if order.isSubmitted():
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))

        # Dispatch events from the trade monitor.
        try:
            eventType, eventData = self.__tradeMonitor.getQueue().get(True, LiveBroker.QUEUE_TIMEOUT)

            if eventType == TradeMonitor.ON_USER_TRADE:
                return self._onUserTrades(eventData)
            else:
                common.logger.error("Invalid event received to dispatch: %s - %s" % (eventType, eventData))
        except Queue.Empty:
            pass

    def peekDateTime(self):
        # Return None since this is a realtime subject.
        return None

    # END observer.Subject interface

    # BEGIN broker.Broker interface

    def getCash(self, includeShort=True):
        return self.__cash

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def getShares(self, instrument):
        return self.__shares.get(instrument, 0)

    def getPositions(self):
        return self.__shares

    def getActiveOrders(self, instrument=None):
        return self.__activeOrders.values()

    @liveUtils.tryForever
    def submitOrder(self, order):
        if order.isInitial():
            # Override user settings based on Bitstamp limitations.
            order.setAllOrNone(False)
            order.setGoodTillCanceled(True)

            if order.isBuy():
                bitstampOrder = self.__httpClient.buyLimit(order.getLimitPrice(), order.getQuantity())
            else:
                bitstampOrder = self.__httpClient.sellLimit(order.getLimitPrice(), order.getQuantity())

            order.setSubmitted(bitstampOrder.getId(), bitstampOrder.getDateTime())
            self._registerOrder(order)
            # Switch from INITIAL -> SUBMITTED
            # IMPORTANT: Do not emit an event for this switch because when using the position interface
            # the order is not yet mapped to the position and Position.onOrderUpdated will get called.
            order.switchState(broker.Order.State.SUBMITTED)
        else:
            raise Exception("The order was already processed")

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        raise Exception("Market orders are not supported")

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        if instrument != common.btc_symbol:
            raise Exception("Only BTC instrument is supported")

        if action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        elif action == broker.Order.Action.SELL_SHORT:
            action = broker.Order.Action.SELL

        if action not in [broker.Order.Action.BUY, broker.Order.Action.SELL]:
            raise Exception("Only BUY/SELL orders are supported")

        instrumentTraits = self.getInstrumentTraits(instrument)
        limitPrice = round(limitPrice, 2)
        quantity = instrumentTraits.roundQuantity(quantity)
        return broker.LimitOrder(action, instrument, limitPrice, quantity, instrumentTraits)

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        raise Exception("Stop orders are not supported")

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        raise Exception("Stop limit orders are not supported")

    @liveUtils.tryForever
    def cancelOrder(self, order):
        activeOrder = self.__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception("The order is not active anymore")
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")

        self.__httpClient.cancelOrder(order.getId())
        self._unregisterOrder(order)
        order.switchState(broker.Order.State.CANCELED)

        # Update cash and shares.
        self.refreshAccountBalance()

        # Notify that the order was canceled.
        self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, "User requested cancellation"))

    # END broker.Broker interface
