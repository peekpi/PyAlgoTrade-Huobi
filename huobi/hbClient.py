from liveApi.TradeClientBase import *
from liveApi.liveUtils import *
from pyalgotrade.utils import dt

from hbsdk import ApiClient, ApiError

from ApiKey import API_KEY
from ApiKey import API_SECRET

def Str2float(func):
    def waper(*args, **kwargs):
        return float(func(*args, **kwargs))
    return waper

class hbOrderType():
    BuyLimit   = 'buy-limit'
    BuyMarket  = 'buy-market'
    SellLimit  = 'sell-limit'
    SellMarket = 'sell-market'

class hbOrderState():
    OrderFilled = 'filled'
    OrderCanceled = 'canceled'
    OrderSubmited = 'submitted'

class hbTradeOrder(TradeOrderBase):
    def __init__(self, obj):
        self.__obj = obj
        super(hbTradeOrder, self).__init__()

    def getId(self):
        return self.__obj.id
    def isBuy(self):
        return self.__obj.type in (hbOrderType.BuyLimit, hbOrderType.BuyMarket)
    def isSell(self):
        return not self.isBuy()
    @Str2float
    def getPrice(self):
        return self.__obj.price
    @Str2float
    def getAmount(self):
        return self.__obj.amount
    def getDateTime(self):
        return dt.timestamp_to_datetime(int(self.__obj['created-at'])/1000)

# GET /v1/order/orders/{order-id}/matchresults
class hbTradeUserTransaction(TradeUserTransactionBase):
    def __init__(self, obj):
        self.__obj = obj
    @Str2float
    def getBTC(self):
        return self.__obj['field-amount']
    @Str2float
    def getBTCUSD(self):
        #return self.__obj['field-cash-amount']
        return self.__obj['price']
    @Str2float
    def getFee(self):
        return self.__obj['field-fees']
    def getOrderId(self):
        return self.__obj['id']
    def isFilled(self):
        return self.__obj['state'] == hbOrderState.OrderFilled
    def getDateTime(self):
        return dt.timestamp_to_datetime(int(self.__obj['finished-at'])/1000)

class hbTradeAccountBalance(TradeAccountBalanceBase):
    def __init__(self, obj):
        self.__obj = obj
        
    def getUSDAvailable(self):
        return self.__obj['usdt']
    def getBTCAvailable(self):
        return self.__obj['coin']

class hbCoinType():
    def __init__(self, coin, cash):
        self.__coin = coin
        self.__cash = cash
        self.__symbol = coin+cash
    def getCoin(self):
        return self.__coin
    def getCash(self):
        return self.__cash
    def getSymbol(self):
        return self.__symbol
    def __str__(self):
        return self.getSymbol()

class hbAccountBalance():
    def __init__(self, instrument, obj):
        self.__coin = 0
        self.__cash = 0
        balances = obj.get('list')
        if balances is None:
            return
        for x in balances:
            if x.currency == instrument.getCoin() and x.type == 'trade':
                self.__coin = x.balance
            elif x.currency == instrument.getCash() and x.type == 'trade':
                self.__cash = x.balance
    @Str2float
    def getCash(self):
        return self.__cash
    @Str2float
    def getCoin(self):
        return self.__coin

class hbTradeClient(TradeClientBase):
    def __init__(self, instrument):
        self.__coinType = instrument
        self.__client = ApiClient(API_KEY, API_SECRET)
        self.__accountid = self.getAccountId()

    @tryForever
    def getAccountId(self):
        accs = self.__client.get('/v1/account/accounts')
        for x in accs:
            if x.type == 'spot' and x.state == 'working':
                return x.id
        raise Exception('no active account ID!')
        
    # --
    #@exceDebug
    def getAccountBalance(self):
        balances = self.__client.get('/v1/account/accounts/%s/balance' % self.__accountid)
        acc = hbAccountBalance(self.__coinType, balances)
        print('--getAccountBalance: usdt:%s coin:%s'%(acc.getCash(), acc.getCoin()))
        return hbTradeAccountBalance({'usdt':acc.getCash(), 'coin':acc.getCoin()})

    # --
    #@exceDebug
    def getOpenOrders(self):
        print('--getOpenOrders:')
        return []
        '''
        return [hbTradeOrder({
            'id': ID(),
            'isBuy' : True,
            'price' : 13990.99,
            'amount' : 1.1234,
            'time' : datetime.datetime.utcnow(),
        })]
        '''

    # --
    #@exceDebug
    def cancelOrder(self, orderId):
        print('--cancelOrder:%s'%orderId)
        self.__client.post('/v1/order/orders/%s/submitcancel' % orderId)
        self.checkOrderState(orderId, [hbOrderState.OrderCanceled, hbOrderState.OrderFilled])

    # --
    #@exceDebug
    def buyLimit(self, limitPrice, quantity):
        print('--buyLimit:%s %s'%(limitPrice, quantity))
        orderInfo = self.postOrder(limitPrice, quantity, hbOrderType.BuyLimit)
        return hbTradeOrder(orderInfo)

    # --
    #@exceDebug
    def sellLimit(self, limitPrice, quantity):
        print('--sellLimit:%s %s'%(limitPrice, quantity))
        orderInfo = self.postOrder(limitPrice, quantity, hbOrderType.SellLimit)
        return hbTradeOrder(orderInfo)

    # --
    #@exceDebug
    def getUserTransactions(self, ordersId):
        if len(ordersId):
            print('--getUserTransactions:%s'%ordersId)
        ret = []
        for oid in ordersId:
            orderInfo = self.__client.get('/v1/order/orders/%s' % oid)
            ret.append(hbTradeUserTransaction(orderInfo))
        return ret

    def postOrder(self, limitPrice, quantity, orderType):
        price = str(PriceRound(limitPrice))
        amount = str(CoinRound(quantity))
        order_id = self.__client.post('/v1/order/orders', {
            'account-id': self.__accountid,
            'amount': amount,
            'price': price,
            'symbol': self.__coinType.getSymbol(),
            'type': orderType,
            'source': 'api'
        })
        self.activeOrder(order_id)
        orderInfo = self.checkOrderState(order_id, [hbOrderState.OrderSubmited, hbOrderState.OrderFilled])
        return orderInfo

    @tryForever
    def checkOrderState(self, orderid, states):
        orderInfo = self.__client.get('/v1/order/orders/%s' % orderid)
        if orderInfo.state in states:
            return orderInfo
        raise Exception('wait state:%s => %s'%(orderInfo.state, states))

    @tryForever
    def activeOrder(self, orderid):
        return self.__client.post('/v1/order/orders/%s/place' % orderid)


