# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import time
import datetime
import threading
import Queue

from pyalgotrade import bar
from pyalgotrade import barfeed
from pyalgotrade import dataseries
from pyalgotrade import resamplebase
import pyalgotrade.logger
from pyalgotrade.utils import dt
import api


logger = pyalgotrade.logger.getLogger("xignite")


def utcnow():
#    return dt.as_utc(datetime.datetime.utcnow())
    return dt.as_utc(datetime.datetime.now())


class PollingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__stopped = False

    def __wait(self):
        # Wait until getNextCallDateTime checking for cancelation every 0.5 second.
        nextCall = self.getNextCallDateTime()
#        nextCall = self.getNextCallDateTime() - datetime.timedelta(seconds=3600)
        print("nextTime:%s"%nextCall)
        while not self.__stopped and utcnow() < nextCall:
            time.sleep(0.5)

    def stop(self):
        self.__stopped = True

    def stopped(self):
        return self.__stopped

    def run(self):
        logger.debug("Thread started.")
        while not self.__stopped:
            self.__wait()
            if not self.__stopped:
                try:
                    self.doCall()
                except Exception, e:
                    logger.critical("Unhandled exception", exc_info=e)
        logger.debug("Thread finished.")

    # Must return a non-naive datetime.
    def getNextCallDateTime(self):
        raise NotImplementedError()

    def doCall(self):
        raise NotImplementedError()


def build_bar(barDict, frequency):
    f=lambda x:x[0:4]+"-"+x[4:6]+"-"+x[6:8]+" "+x[8:10]+":"+x[10:12]+":"+x[12:14]
    return bar.BasicBar(f(barDict["Time"]), barDict["Open"], barDict["High"], barDict["Low"], barDict["Close"], barDict["Volume"], None, frequency)


class GetBarThread(PollingThread):

    # Events
    ON_BARS = 1

    def __init__(self, queue, identifiers, frequency, apiCallDelay):
        PollingThread.__init__(self)

        # Map frequency to precision and period.
        if frequency < bar.Frequency.MINUTE:
            raise Exception("Frequency must be greater than or equal to bar.Frequency.MINUTE")
        elif frequency < bar.Frequency.HOUR:
            self.__precision = "Minutes"
            self.__period = frequency / bar.Frequency.MINUTE
        elif frequency < bar.Frequency.DAY:
            self.__precision = "Hours"
            self.__period = frequency / bar.Frequency.HOUR
        else:
            raise Exception("Frequency must be less than bar.Frequency.DAY")

        self.__queue = queue
        self.__identifiers = identifiers
        self.__frequency = frequency
        self.__nextBarClose = None
        # The delay between the bar's close and the API call.
        self.__apiCallDelay = apiCallDelay

        self.__updateNextBarClose()

    def __updateNextBarClose(self):
        self.__nextBarClose = resamplebase.build_range(utcnow(), self.__frequency).getEnding()

    def getNextCallDateTime(self):
        return self.__nextBarClose + self.__apiCallDelay

    def doCall(self):
        endDateTime = self.__nextBarClose
        self.__updateNextBarClose()
        barDict = {}

        for indentifier in self.__identifiers:
            try:
                response = api.XigniteGlobalRealTime_GetBar(indentifier, endDateTime, self.__period)
                # logger.debug(response)
                barDict[indentifier] = build_bar(response["Bar"], self.__frequency)
            except api.XigniteError, e:
                logger.error(e)

        if len(barDict):
            bars = bar.Bars(barDict)
            self.__queue.put((GetBarThread.ON_BARS, bars))


class LiveFeed(barfeed.BaseBarFeed):
    """A real-time BarFeed that builds bars using XigniteGlobalRealTime API
    (https://www.xignite.com/product/global-real-time-stock-quote-data/).

    :param apiToken: The API token to authenticate calls to Xignine APIs.
    :type apiToken: string.
    :param identifiers: A list with the fully qualified identifier for the securities including the exchange suffix.
    :type identifiers: list.
    :param frequency: The frequency of the bars.
        Must be greater than or equal to **bar.Frequency.MINUTE** and less than **bar.Frequency.DAY**.
    :param apiCallDelay: The delay in seconds between the bar's close and the API call.
        This is necessary because the bar may not be immediately available.
    :type apiCallDelay: int.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the opposite end.
    :type maxLen: int.

    .. note:: Valid exchange suffixes are:

         * **ARCX**: NYSE ARCA
         * **CHIX**: CHI-X EUROPE LIMITED
         * **XASE**: NYSE MKT EQUITIES
         * **XNAS**: NASDAQ
         * **XNYS**: NEW YORK STOCK EXCHANGE, INC
    """

    QUEUE_TIMEOUT = 0.01

    def __init__(self, identifiers, frequency, apiCallDelay=30, maxLen=dataseries.DEFAULT_MAX_LEN):
        barfeed.BaseBarFeed.__init__(self, frequency, maxLen)
        if not isinstance(identifiers, list):
            raise Exception("identifiers must be a list")

        self.__queue = Queue.Queue()
        self.__thread = GetBarThread(self.__queue, identifiers, frequency, datetime.timedelta(seconds=apiCallDelay))
        for instrument in identifiers:
            self.registerInstrument(instrument)

    ######################################################################
    # observer.Subject interface

    def start(self):
        if self.__thread.is_alive():
            raise Exception("Already strated")

        # Start the thread that runs the client.
        self.__thread.start()

    def stop(self):
        self.__thread.stop()

    def join(self):
        if self.__thread.is_alive():
            self.__thread.join()

    def eof(self):
        return self.__thread.stopped()

    def peekDateTime(self):
        return None

    ######################################################################
    # barfeed.BaseBarFeed interface

    def getCurrentDateTime(self):
        return utcnow()

    def barsHaveAdjClose(self):
        return False

    def getNextBars(self):
        ret = None
        try:
            eventType, eventData = self.__queue.get(True, LiveFeed.QUEUE_TIMEOUT)
            if eventType == GetBarThread.ON_BARS:
                ret = eventData
            else:
                logger.error("Invalid event received: %s - %s" % (eventType, eventData))
        except Queue.Empty:
            pass
        return ret
