#coding=utf-8

'''
本程序在 Python 3.3.0 环境下测试成功
使用方法：python HuobiMain.py
'''

from Util import *
import HuobiService

if __name__ == "__main__":
    print ("获取账号详情")
#    print (HuobiService.getAccountInfo(ACCOUNT_INFO))
    account = HuobiService.getAccountInfo(ACCOUNT_INFO)
    print type(account)
    print("total:%f"%float(account['total']))
    print ("获取所有正在进行的委托")
    print (HuobiService.getOrders(1,GET_ORDERS))
    print ("获取订单详情")
    print (HuobiService.getOrderInfo(1,4523732186,ORDER_INFO))
    print ("限价买入")
#    print (HuobiService.buy(1,"100","1",None,None,BUY))
    print ("限价卖出")
#    print (HuobiService.sell(2,"100","0.2",None,None,SELL))
    print ("市价买入")
#    print (HuobiService.buyMarket(2,"30",None,None,BUY_MARKET))
    print ("市价卖出")
#    print (HuobiService.sellMarket(2,"1.3452",None,None,SELL_MARKET))
    print ("查询个人最新10条成交订单")
    print (HuobiService.getNewDealOrders(1,NEW_DEAL_ORDERS))
    print ("根据trade_id查询order_id")
    print (HuobiService.getOrderIdByTradeId(1,274424,ORDER_ID_BY_TRADE_ID))
    print ("取消订单接口")
    print (HuobiService.cancelOrder(1,68278313,CANCEL_ORDER))


