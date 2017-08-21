from Util import *
import HuobiService as hapi
from pyalgotrade.broker import Order

class httpClient(object):
    def limitBuy(self, price, amount, tradeid):
        pass;
    def limitSell(self, price, amount, tradeid):
        pass;
    def marketBuy(self, amount, tradeid):
        pass;
    def marketSell(self, amount, tradeid
        pass;

class HuobiClient(httpClient):
    class CoinType(object):
        COIN_BTC = 1
        COIN_LTC = 2
    def __init__(self):
        self.__orders = {}
        self.__cash = 0
        self.__ltc = 0
        self.__btc = 0
        self.__total = 0
        self.updateAccountInfo()

    def __addNewOrder(self, orderId, amount, processed_amount = 0):
        self.__orders[orderId] = [amount, processed_amount]

    def __updateOrder(self, orderId, amount, processed_amount):
        order = self.__orders.get(orderId)
        if order is None:
            __addNewOrder(orderId, amount, processed_amount)
            return
        self.__orders[orderId][1] = processed_amount
        if self.__orders[retId][0] == processed_amount:
            del self.__orders[retId]
            pass
#            finished order
        else:
#           onUpdateOrder
            pass

    def limitBuy(self, price, amount, tradeid):
        ret = hapi.buy(COIN_BTC, str(price), str(amount), None, str(tradeid), BUY)
        if ret['result'] != 'success':
            return None
        return Order(Order.Type.LIMIT, Order.Action.BUY, amount)
        print(ret)
        self.__addNewOrder(ret['id'], amount)

    def limitSell(self, price, amount, tradeid):
        ret = hapi.sell(COIN_BTC, str(price), str(amount), None, str(tradeid), SELL)
        if ret['result'] != 'success':
            return None
        self.__addNewOrder(ret['id'], amount)

    def marketBuy(self, amount, tradeid):
        hapi.buyMarket(COIN_BTC, str(amount), None, str(tradeid), BUY_MARKET)
        if ret['result'] != 'success':
            return None
        self.__addNewOrder(ret['id'], amount)

    def marketSell(self, amount, tradeid):
        hapi.sellMarket(COIN_BTC, str(amount), None, str(tradeid), SELL_MARKET)
        if ret['result'] != 'success':
            return None
        self.__addNewOrder(ret['id'], amount)

    def cancelOrder(self, tradeid):
        ret = hapi.HuobiService.cancelOrders(COIN_BTC, self.__idmap[tradeid], CANCEL_ORDER)
        if ret['result'] != 'success':
            return None

    def updateOrderInfo(self):
        ret = hapi.HuobiService.getOrders(1,GET_ORDERS)
        for order in ret:
            self.__updateOrder(order['id'], float(order['order_amount']), float(order['processed_amount']))

    def updateAccountInfo(self):
        ret = hapi.getAccountInfo(ACCOUNT_INFO)
        self.__total = float(ret['total'])
        self.__cash = float(ret['available_cny_display'])
        self.__ltc = float(ret['available_ltc_display'])
        self.__btc = float(ret['available_btc_display'])
        print(ret)

