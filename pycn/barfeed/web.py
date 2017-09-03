import json
import zlib
import gzip
from StringIO import StringIO
from pyalgotrade.websocket.client import WebSocketClientBase


class HuobiWebSocket(WebSocketClientBase):
    def __init__(self, url):
        super(HuobiWebSocket, self).__init__(url)
        print(url)

    def received_message(self, message):
        buf = StringIO(message.data)
        message.data = gzip.GzipFile(fileobj=buf).read()
        super(HuobiWebSocket, self).received_message(message)

    def onMessage(self, msg):
        ping = msg.get("ping")
        if ping is not None:
            return self.pong(ping)
        tick = msg.get("tick")
        if tick is not None:
            return self.onKline(msg['ts'], tick)

    def onKline(self, timestamp, msg):
        raise NotImplementedError()

    def onOpened(self):
        print("Opend!")
        self.subscribe(1,2)
    def onClosed(self, msg, reason):
        print("onClosed msg:%s reason:%s"%(msg, reason))
    def onUnhandledException(self, exception):
        print("onExcepetion:"%(exception))

    def onDisconnectionDetected(self):
        print("onDisconnectionDetected")

    def subscribe(self, symbol, period):
        msg = { 
                "sub": "market.ltccny.kline.60min",
                "id":"id1"
                }
        self.send(msg)
    def pong(self, pingvalue):
        self.send({"pong":pingvalue})
    def send(self, dic):
        super(HuobiWebSocket, self).send(json.dumps(dic), False)

