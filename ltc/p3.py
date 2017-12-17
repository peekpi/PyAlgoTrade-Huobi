import pandas as pd
import json
import time

from hbsdk import ApiClient, ApiError

API_KEY = "API_KEY"
API_SECRET = "API_SECRET"

SYMBOL='ltcusdt'
PREIOD = 60

client = ApiClient(API_KEY, API_SECRET)
history = client.mget('/market/history/kline', symbol=SYMBOL, period='%dmin'%PREIOD, size=2000)
print(len(history))

def dtf(x):
    time_local = time.localtime(x)
    return time.strftime("%Y-%m-%d %H:%M:%S",time_local)

def rf(x):
    return [dtf(x.id), x.open, x.high, x.low, x.close, x.vol, x.close]

def redf(x,y):
    return x+[rf(y)]

jdict= reduce(redf, history, [])
print(len(jdict))

headList=["Date Time","Open","High","Low","Close","Volume","Adj Close"]

#df = pd.DataFrame.from_dict(jdict,{"Date,Open,High,Low,Close,Volume,Adj Close"})
df = pd.DataFrame.from_dict(jdict)
df.to_csv("2000.csv",index=False, header=headList)
