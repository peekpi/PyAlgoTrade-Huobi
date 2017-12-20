__e = True
def exce(fn):
    def waper(*args, **kwargs):
        global __e
        if __e is True:
            __e = False
            raise Exception(fn.__name__)
        __e = True
        return fn(*args, **kwargs)
    return waper

class tradeApi():
    @exce
    def getAccountInfo(self, *args, **kw):
        return {'available_money':50000, 'available_coin':5}
    @exce
    def getOrders(self, *args, **kw):
        return []
    @exce
    def cancelOrder(self, *args, **kw):
        pass
    @exce
    def buyLimit(self, *args, **kw):
        pass
    @exce
    def sellLimit(self, *args, **kw):
        pass
    @exce
    def getOrderInfo(self, *args, **kw):
        pass

