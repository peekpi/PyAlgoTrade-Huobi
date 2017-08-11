#coding:utf-8
import pandas
import json
import urllib2

def getHuobiData(type, period, length):
    """返回list格式数据
    """
    url ="http://api.huobi.com/staticmarket/"+type+"_kline_"+period+"_json.js?length="+length 
    print(url)
    fstr=urllib2.urlopen(url).read()
    jlist=json.loads(fstr)
    #火币最后一组数据中的交易量有问题，删掉
    jlist.pop()
    return jlist 

def getCvs(type,period,length):
    """生成CVS文件
    """
    jlist=getHuobiData(type, period, length)
    f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]+" "+x[8:10]+":"+x[10:12]+":"+x[12:14]

    for x in jlist:
        x[0] = f(x[0])
    df = pandas.DataFrame.from_dict(jlist)
    filename = "%s_%s.csv" % (type, period)
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
    getCvs("btc","001","2000")
    getCvs("btc","005","2000")
    getCvs("btc","015","2000")
    getCvs("btc","030","2000")
    getCvs("btc","060","2000")
    getCvs("btc","100","2000")
    getCvs("btc","200","2000")
    getCvs("btc","300","2000")
    getCvs("btc","400","2000")

    getCvs("ltc","001","2000")
    getCvs("ltc","005","2000")
    getCvs("ltc","015","2000")
    getCvs("ltc","030","2000")
    getCvs("ltc","060","2000")
    getCvs("ltc","100","2000")
    getCvs("ltc","200","2000")
    getCvs("ltc","300","2000")
    getCvs("ltc","400","2000")
    pass

def dataToStr(list):
    """废弃 用join函数可替代
    """
    line  = ""
    for item in list:
        line += str(item)+","
    return line[:-1] 


def updateCsv(cointype, period, length):
    """更新单个csv文件
    按需求获取k线数据后与本地cvs对比并更新
    """

    jlist = getHuobiData(cointype, period, length)
    filename = "%s_%s.csv" % (cointype, period)
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


def updateAllCsv():
    """更新所有的cvs文件
    """
    updateCsv("btc","001","2000")
    updateCsv("btc","005","2000")
    updateCsv("btc","015","2000")
    updateCsv("btc","030","2000")
    updateCsv("btc","060","2000")
    updateCsv("btc","100","2000")
    updateCsv("btc","200","2000")
    updateCsv("btc","300","2000")
    updateCsv("btc","400","2000")
    updateCsv("ltc","001","2000")
    updateCsv("ltc","005","2000")
    updateCsv("ltc","015","2000")
    updateCsv("ltc","030","2000")
    updateCsv("ltc","060","2000")
    updateCsv("ltc","100","2000")
    updateCsv("ltc","200","2000")
    updateCsv("ltc","300","2000")
    updateCsv("ltc","400","2000")
    pass
    
#第一次跑要先初始化数据
#initCsv()
updateAllCsv()
