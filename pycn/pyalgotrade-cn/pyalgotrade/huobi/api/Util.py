#coding=utf-8

import urllib
import hashlib
import hmac
import base64

#在此输入您的Key
ACCESS_KEY = "665bc788-1ce3fcec-74da9853-dde95"
SECRET_KEY = "1857b962-e9b222a9-bf385837-7e2d8"

HUOBI_SERVICE_API="https://api.huobi.com/apiv3"

BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
ACCOUNT_INFO = "get_account_info"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
SELL = "sell"
SELL_MARKET = "sell_market"
COIN_BTC = 1
COIN_LTC = 2

def signature(params):
    params = sorted(params.iteritems(), key=lambda d:d[0], reverse=False)
    message = urllib.urlencode(params)
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig=m.hexdigest()
    return sig

