### 读我

居然有人看，那就写一下吧。  
这个工程是基于*pyalogtrade 0.18*的，我做了火币pro实时交易的对接，放github只是方便同步，不过既然有人看，那就简单写一下说明。

工程分两个部分：回测和实盘。

#### 回测
源码位置：

- RegressionTest

回测测试：

1. 获取历史K线：`python getKlines.py`
2. 根据策略回测：`python 3.py`

BTCUSDT回测图：
![回测图][examplePng]
> 这只是一个简单的策略，回测效果好的原因是BTC一直在涨。。。

#### 实盘
源码位置：

- huobi

实盘测试：`python 3.py`

> ***注意，填入正确的API KEY后，运行这个脚本可能会造成财产损失！***

>> - 实盘只支持单币种交易,如BTCUSDT、LTCUSDT等等
>> - 有一些接口实现的不是很好，不过功能上是没问题的，后续会慢慢更新。

### 安装指南

以ubuntu为例：

1. 安装python 2.7和python-pip：  
`sudo apt-get install python python-pip`
2. 安装pyalgotrade  
`sudo pip install pyalgotrade`
3. 下载上述提到的几个文件，并按照测试步骤测试。

> [pyalgotrade官网][pat_official]  
> [pyalgotrade官方文档][pat_official_doc]

[pat_official]: http://gbeced.github.io/pyalgotrade
[pat_official_doc]: http://gbeced.github.io/pyalgotrade/docs/v0.18/html
[examplePng]: /example.png






