#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime

from hbsdk import ApiClient, ApiError

API_KEY = '29dcf8f8-94118ccd-f6bc8ad0-33e70'
API_SECRET = '9dcd7cd8-6847eea7-d4464751-a9493'

def main():
    client = ApiClient(API_KEY, API_SECRET)
    # get symbol:
    symbols = client.mget('/v1/common/symbols')
    for x in symbols:
        if x['quote-currency'] == 'usdt':
            print '%s\t%s\t%s\t%s\t%s'%(x['base-currency'],x['quote-currency'],x['price-precision'],x['amount-precision'],x['symbol-partition'])
    currencys = client.mget('/v1/common/currencys')
    print(currencys)
    timestamp = client.mget('/v1/common/timestamp')
    print(datetime.datetime.fromtimestamp(int(timestamp)/1000))
    # get user info:
    accs = client.get('/v1/account/accounts')
    for x in accs:
        if x.type == 'spot' and x.state == 'working':
            acc = x
    print(acc)
    print('-------------------------------')
    buy_order_id = client.post('/v1/order/orders', {
        'account-id': acc.id,
        'amount': '0.02',
        'price': '222.21',
        'symbol': 'ltcusdt',
        'type': 'buy-limit',
        'source': 'api'
    })
    print buy_order_id
    print client.get('/v1/order/orders/%s' % buy_order_id)
    try:
        print client.post('/v1/order/orders/%s/place' % buy_order_id)
    except:
        pass
    print client.get('/v1/order/orders/%s' % buy_order_id)
    print('-------------------------------')
    sell_order_id = client.post('/v1/order/orders', {
        'account-id': acc.id,
        'amount': '0.02',
        'price': '222.21',
        'symbol': 'ltcusdt',
        'type': 'sell-limit',
        'source': 'api'
    })
    print sell_order_id
    print client.get('/v1/order/orders/%s' % sell_order_id)
    try:
        print client.post('/v1/order/orders/%s/place' % sell_order_id)
    except:
        pass
    print client.get('/v1/order/orders/%s' % sell_order_id)
    print('-------------------------------')
    client.post('/v1/order/orders/%s/submitcancel' %(buy_order_id))
    print client.get('/v1/order/orders/%s' % buy_order_id)
    print('-------------------------------')
    client.post('/v1/order/orders/%s/submitcancel' %(sell_order_id))
    print client.get('/v1/order/orders/%s' % sell_order_id)
    exit()






    userinfo = client.get('/v1/users/user')
    print(userinfo)
    # get all accounts:
    accs = client.get('/v1/account/accounts')
    print(accs)
    account_id = accs[0].id
    for acc in accs:
        subaccs = client.get('/v1/account/accounts/%s/balance' % acc.id)
        print(subaccs)
    time.sleep(2.0)
    # create order:
    order_id = client.post('/v1/order/orders', {
        'account-id': account_id,
        'amount': '0.02',
        'price': '1020.21',
        'symbol': 'ethcny',
        'type': 'buy-limit',
        'source': 'api'
    })
    print(order_id)
    # place order:
    client.post('/v1/order/orders/%s/place' % order_id)
    # get order details:
    order_info = client.get('/v1/order/orders/%s' % order_id)
    print(order_info)
    # cancel order:
    client.post('/v1/order/orders/%s/submitcancel' % order_id)
    # query order details:
    time.sleep(5.0)
    order_info = client.get('/v1/order/orders/%s' % order_id)
    print(order_info)

if __name__ == '__main__':
    main()
