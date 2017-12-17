#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback
import time

from hbsdk import ApiClient, ApiError

API_KEY = "API_KEY"
API_SECRET = "API_SECRET"

SYMBOL='ltcusdt'

def main():
    client = ApiClient(API_KEY, API_SECRET)
    # get symbol:
    __last_ts = None
    __repeat_ts = None
    __sell_num = 0
    __buy_num = 0

    totalSellPrice1=0
    totalBuyPrice1=0
    totalSellPrice=0
    totalBuyPrice=0
    _earn = 0
    _earn1 = 0
    while True:
        try:
            tradeDetail = client.mget('/market/trade', symbol=SYMBOL, rkey='tick')
            ts = tradeDetail.ts
            if __repeat_ts == ts:
                print('FUCK!')
                continue
            __repeat_ts = ts
            __ts = ts/1000%3600/60
            print('-----------%d--%d-%d-%d----------'%(ts, __ts, __sell_num, __buy_num))

            avgSellPrice = totalSellPrice/__sell_num if __sell_num else 0
            avgSellPrice1 = totalSellPrice1/__sell_num if __sell_num else 0
            avgBuyPrice = totalBuyPrice/__buy_num if __buy_num else 0
            avgBuyPrice1 = totalBuyPrice1/__buy_num if __buy_num else 0
            print('avg sellPrice:%f %f'%(avgSellPrice, avgSellPrice1))
            print('avg buyPrice:%f %f'%(avgBuyPrice, avgBuyPrice1))
            #print(detail.data)
            if __last_ts == __ts:
                for x in tradeDetail.data:
                    print('%s:%f %f -- %f'%(x.direction, x.price, x.amount, sellPrice if x.direction == 'buy' else buyPrice))
                    if __buy_num > __sell_num and x.price >= sellPrice:
                        totalSellPrice += sellPrice
                        totalSellPrice1 += x.price
                        __sell_num += 1
                        print('Sellout:%f'%sellPrice)
                        break
                    elif __buy_num == __sell_num and x.price <= buyPrice:
                        __buy_num += 1
                        totalBuyPrice += buyPrice
                        totalBuyPrice1 += x.price
                        print('Buyin:%f'%buyPrice)
                        break
                continue

            k0,k1 = client.mget('/market/history/kline', symbol=SYMBOL, period='60min', size=2)
            #merge = client.mget('/market/detail/merged', rkey='tick', symbol=SYMBOL)
            depth = client.mget('/market/depth', rkey='tick', symbol=SYMBOL, type='step5')
            tamount= k0.amount*60/__ts if __ts else k1.amount
            print(k0.amount)
            print(k1.amount)
            print(tamount)
            print((tamount+k1.amount)/2)
            print((tamount+k1.amount)/120/2)
            avgCount = (tamount+k1.amount)/240/0.9
            #print(merge)

            '''
            if __sell_num == __buy_num:
                _buyCount = _sellCount = avgCount / 2
            elif __sell_num > __buy_num:
                _sellCount = avgCount * __sell_num / ( __sell_num + __buy_num ) * 0.61
                _buyCount = avgCount - _sellCount
            else:
                _buyCount = avgCount * __buy_num / ( __sell_num + __buy_num ) * 0.61
                _sellCount = avgCount - _buyCount
            '''
            _buyCount = _sellCount = avgCount / 2

            sellPrice = sellCount = 0
            for price,count in depth.asks:
                if sellCount + count >= _sellCount:
                    #_sellPrice = ( price - sellPrice ) * ( ( _sellCount - sellCount ) / count )
                    #sellPrice = sellPrice + _sellPrice if sellPrice else price - 0.01
                    sellPrice = price - 0.01
                    print('sellPrice:%.2f tCount:%f cCount:%f avgCount:%f'%(price, sellCount, count, _sellCount))
                    break
                sellPrice = price
                sellCount += count

            buyPrice = buyCount = 0
            for price,count in depth.bids:
                if buyCount + count >= _buyCount:
                    #_buyPrice = ( buyPrice - price ) * ( ( _buyCount - buyCount ) / count )
                    #buyPrice = buyPrice - _buyPrice if buyPrice else price + 0.01
                    buyPrice += 0.01
                    print('buyPrice:%.2f tCount:%f cCount:%f avgCount:%f'%(price, buyCount, count, _buyCount))
                    break
                buyPrice = price
                buyCount += count

            diff = sellPrice - buyPrice
            if diff < sellPrice*0.005:
                diff=sellPrice*0.005-diff
                sellPrice+=diff/2
                buyPrice-=diff/2
                diff = sellPrice-buyPrice
                print('---Warning:adjust price!')

            print('Order sell: %.2f %.2f %.2f %.2f'%(sellPrice, sellCount, diff, diff*100/sellPrice))
            print('Order buy : %.2f %.2f %.2f %.2f'%(buyPrice, buyCount, diff, diff*100/buyPrice))
            __last_ts = __ts
        except:
            print('------------EXCEPT------------')
            print(traceback.print_exc())
            print('------------======------------')
            pass
        finally:
            time.sleep(1)
if __name__ == '__main__':
    main()
