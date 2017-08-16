#coding:utf-8

"""python 2.7
"""

import pandas
import json
import urllib2
import time
import os

g_coinType=["ltc","btc"]
g_period=["001","005","015","030","060","100","200","300","400"]
def TypePeriodGen():
    return ((c,p) for c in g_coinType for p in g_period)

def getHuobiData(coinType, period, length):
    """返回list格式数据
    """
    url ="http://api.huobi.com/staticmarket/%s_kline_%s_json.js?length=%d"%(coinType, period, length) 
    print(url)
    fstr=urllib2.urlopen(url).read()
    jlist=json.loads(fstr)
    #火币最后一组数据中的交易量有问题，删掉
    jlist.pop()
    return jlist 

def getCvs(coinType,period,length):
    """生成CVS文件
    """
    jlist=getHuobiData(coinType, period, length)
    f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]+" "+x[8:10]+":"+x[10:12]+":"+x[12:14]

    for x in jlist:
        x[0] = f(x[0])
    df = pandas.DataFrame.from_dict(jlist)
    filename = "%s_%s.csv" % (coinType, period)
    df.to_csv(filename,index=False, header=["Date Time","Open","High","Low","Close","Volume"])
    return filename

def getLastDataFromCvs(fileName):
    """获取cvs文件最后一行数据
    """
    with open(fileName) as f:
        off=-50
        while True:
            f.seek(off,2)
            lines=f.readlines()
            if(len(lines)>=2):
                return lines[-1]
            else:
                off*=2
    pass
    

def initCsv():
    """初始化可以拿到的最老数据
    """
    map(lambda x:getCvs(x[0], x[1], 2000), TypePeriodGen())
    
def dataToStr(list):
    """废弃 用join函数可替代
    """
    line  = ""
    for item in list:
        line += str(item)+","
    return line[:-1] 


def updateCsv(coincoinType, period, length):
    """更新单个csv文件
    按需求获取k线数据后与本地cvs对比并更新
    """

    jlist = getHuobiData(coincoinType, period, length)
    filename = "%s_%s.csv" % (coincoinType, period)
    lastline = getLastDataFromCvs(filename)
    #废弃 lastDateTime = lastline.split(",")[0].replace("-","").replace(":","").replace(" ","")
    #初始化的时候把api提供的参数截掉了后三位，待会过滤的时候还要用
    lastDateTime = lastline.split(",")[0].translate(None,'-: ') + '000'
    print("lastLine %s" % lastline)
    print("lastDateTime %s" % lastDateTime)

    f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]+" "+x[8:10]+":"+x[10:12]+":"+x[12:14]
    updateList=[]
    for data in jlist:
        if(lastDateTime < data[0]):
            data[0]=f(str(data[0]))
            #废弃 print(dataToStr(data))
            updateList.append(",".join(str(s) for s in data))

    print("更新数据:")
    print(updateList)
    with open(filename,'a') as fout:
        fout.writelines(line+'\n' for line in updateList)
    print("更新%s条" % len(updateList))
    pass


def updateAllCsv(length):
    """更新所有的cvs文件
    length最长为2000
    """
    map(lambda x:updateCsv(x[0], x[1], length), TypePeriodGen())
   
def getTime():
    return time.strftime('%Y-%m-%d %X',time.localtime())

#第一次跑要先初始化数据
if 'btc_001.csv' not in os.listdir('.'):
    initCsv()
while True:
    print "%s 开始更新" % getTime()
    updateAllCsv(50)
    minutes=30
    print "%s 更新完毕 %s分钟后再次更新" % (getTime(),minutes)
    time.sleep(60 * minutes)
