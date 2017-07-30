import pandas as pd
import json

fstr = open('100.js').read()
jdict=json.loads(fstr)
f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]
for x in jdict:
    x[0] = f(x[0])
    x.append(x[4])
#df = pd.DataFrame.from_dict(jdict,{"Date,Open,High,Low,Close,Volume,Adj Close"})
df = pd.DataFrame.from_dict(jdict)
df.to_csv("100.csv",index=False, header=["Date","Open","High","Low","Close","Volume","Adj Close"])
