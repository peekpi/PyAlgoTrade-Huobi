#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from hbsdk import ApiClient, ApiError

API_KEY = "API_KEY"
API_SECRET = "API_SECRET"

SYMBOL='btcusdt'

PREIOD = 15

def cals(p1, p2):
    return (p2-p1)*100/p1
    #return (p1-p2)*100/p2 if p1 > p2 else (p2-p1)*100/p1

def main():
    print('-----------------------------%d'%PREIOD)
    client = ApiClient(API_KEY, API_SECRET)
    history = client.mget('/market/history/kline', symbol=SYMBOL, period='%dmin'%PREIOD, size=2000)
    i = 0
    n = 0
    t = 0
    for x in history:
        c = cals(x.open, x.high)
        if c > 0.4:
            print('%05d: %02d-%02d %f'%(n, i*PREIOD/60, i*PREIOD%60, c))
            n += 1
            t+=c
        i+=1
    print('%f %f'%(n/2000.0,t/n))

if __name__ == '__main__':
    main()
