#!/bin/sh
#wget http://api.huobi.com/staticmarket/btc_kline_${1}_json.js?length=$2 -O 2000.js
wget http://api.huobi.com/staticmarket/ltc_kline_${1}_json.js?length=$2 -O 2000.js
python3 p3.py
