import pandas as pd
import json

fstr = open('2000.js').read()
jdict=json.loads(fstr)

f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]
headList=["Date","Open","High","Low","Close","Volume","Adj Close"]
if True:
    f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]+" "+x[8:10]+":"+x[10:12]+":"+x[12:14]
    headList[0] = "Date Time"

for x in jdict:
    x[0] = f(x[0])
    x.append(x[4])
#df = pd.DataFrame.from_dict(jdict,{"Date,Open,High,Low,Close,Volume,Adj Close"})
df = pd.DataFrame.from_dict(jdict)
df.to_csv("2000.csv",index=False, header=headList)

#data open hith  low close
#         ||
#data open close low high
f=lambda x:[x[0],x[1],x[4],x[3],x[2]]
jsa=map(f, jdict)
st=json.dump(jsa, file('/tmp/data.js','w'))
