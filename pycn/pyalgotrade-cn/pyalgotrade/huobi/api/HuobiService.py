#coding=utf-8

import time

import requests

from huobi.Util import *

import json

def post_retry(payload):
    while True:
        try:
            return post_retry(payload)
            if r.status_code == 200:
                return r.json()
            continue
        except:
            continue
    

'''
获取账号详情
'''
def getAccountInfo(method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"method":method}
    sign=signature(params)
    params['sign']=sign

    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
下单接口
@param coinType
@param price
@param amount
@param tradePassword
@param tradeid
@param method
'''
def buy(coinType,price,amount,tradePassword,tradeid,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"price":price,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
提交市价单接口
@param coinType
@param amount
@param tradePassword
@param tradeid
'''

def buyMarket(coinType,amount,tradePassword,tradeid,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
撤销订单
@param coinType
@param id
'''

def cancelOrder(coinType,id,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"id":id,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
查询个人最新10条成交订单
@param coinType
'''
def getNewDealOrders(coinType,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
根据trade_id查询oder_id
@param coinType
@param tradeid
'''
def getOrderIdByTradeId(coinType,tradeid,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"trade_id":tradeid}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
获取所有正在进行的委托
@param coinType
'''
def getOrders(coinType,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
获取订单详情
@param coinType
@param id
'''
def getOrderInfo(coinType,id,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"method":method,"id":id}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
限价卖出
@param coinType
@param price
@param amount
@param tradePassword
@param tradeid
'''
def sell(coinType,price,amount,tradePassword,tradeid,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"price":price,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    del params['secret_key']
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    payload = urllib.urlencode(params)
    return post_retry(payload)

'''
市价卖出
@param coinType
@param amount
@param tradePassword
@param tradeid
'''
def sellMarket(coinType,amount,tradePassword,tradeid,method):
    timestamp = long(time.time())
    params = {"access_key": ACCESS_KEY,"secret_key": SECRET_KEY, "created": timestamp,"coin_type":coinType,"amount":amount,"method":method}
    sign=signature(params)
    params['sign']=sign
    if tradePassword:
        params['trade_password']=tradePassword
    if tradeid:
        params['trade_id']=tradeid

    del params['secret_key']

    payload = urllib.urlencode(params)
    return post_retry(payload)

