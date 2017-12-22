from liveApi.TradeClientBase import *
from liveApi.liveUtils import exceDebug

__id = 0
def ID():
    global __id
    __id += 1
    return __id

class hbTradeOrder(TradeOrderBase):
    def __init__(self, obj):
        self.__obj = obj
        super(hbTradeOrder, self).__init__()

    def getId(self):
        return self.__obj['id']
    def isBuy(self):
        return self.__obj['isBuy']
    def isSell(self):
        return not self.__obj['isBuy']
    def getPrice(self):
        return self.__obj['price']
    def getAmount(self):
        return self.__obj['amount']
    def getDateTime(self):
        return super(hbTradeOrder, self).getDateTime()

class hbTradeUserTransaction(TradeUserTransactionBase):
    def __init__(self, obj):
        self.__obj = obj
        super(hbTradeUserTransaction, self).__init__()

    def getBTC(self):
        return self.__obj['BTC']
    def getBTCUSD(self):
        return self.__obj['USDT']
    def getFee(self):
        return self.__obj['fee']
    def getOrderId(self):
        return self.__obj['id']
    def isFilled(self):
        return self.__obj['isFilled']
    def getDateTime(self):
        return super(hbTradeUserTransaction, self).getDateTime()

class hbTradeAccountBalance(TradeAccountBalanceBase):
    def __init__(self, obj):
        self.__obj = obj
        
    def getUSDAvailable(self):
        return self.__obj['usdt']
    def getBTCAvailable(self):
        return self.__obj['coin']

class hbTradeClient(TradeClientBase):
    # --
    @exceDebug
    def getAccountBalance(self):
        print('--getAccountBalance: usdt:%s coin:%s'%(50000, 5))
        return hbTradeAccountBalance({'usdt':50000, 'coin':5})

    # --
    @exceDebug
    def getOpenOrders(self):
        
        print('--getOpenOrders: []')
        return [hbTradeOrder({
            'id': ID(),
            'isBuy' : True,
            'price' : limitPrice,
            'amount' : quantity,
            'time' : datetime.datetime.utcnow(),
        })]

    # --
    @exceDebug
    def cancelOrder(self, orderId):
        print('--cancelOrder:%s=>%s'%(type(orderId), orderId))

    # --
    @exceDebug
    def buyLimit(self, limitPrice, quantity):
        print('--buyLimit:%s=>%s %s=>%s'%(type(limitPrice), limitPrice, type(quantity), quantity))
        return hbTradeOrder({
            'id': ID(),
            'isBuy' : True,
            'price' : limitPrice,
            'amount' : quantity,
            'time' : datetime.datetime.utcnow(),
        })

    # --
    @exceDebug
    def sellLimit(self, limitPrice, quantity):
        print('--sellLimit:%s=>%s %s=>%s'%(type(limitPrice), limitPrice, type(quantity), quantity))
        return hbTradeOrder({
            'id': ID(),
            'isBuy' : False,
            'price' : limitPrice,
            'amount' : quantity,
            'time' : datetime.datetime.utcnow(),
        })

    # --
    @exceDebug
    def getUserTransactions(self, ordersId):
        print('--getUserTransactions:%s'%ordersId)

        return [hbTradeUserTransaction({'BTC':0.1, 'USDT':16888, 'fee':0.0002, 'id':x, 'isFilled':False}) for x in ordersId]
