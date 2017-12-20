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
import commonApi as api
import liveUtils


logger = pyalgotrade.logger.getLogger("xignite")


class liveBar(bar.BasicBar):
    def __init__(self, barDict, frequency):
        self.__DateTimeLocal = liveUtils.timestamp_to_DateTimeLocal(barDict["Timestamp"])
        super(liveBar, self).__init__(dt.timestamp_to_datetime(barDict["Timestamp"]), barDict["Open"], barDict["High"], barDict["Low"], barDict["Close"], barDict["Volume"], None, frequency)
    def getDateTimeLocal(self):
        return self.__DateTimeLocal

class PollingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__stopped = False

    def __wait(self):
        # Wait until getNextCallDateTime checking for cancelation every 0.5 second.
        nextCall = self.getNextCallDateTime()
#        nextCall = self.getNextCallDateTime() - datetime.timedelta(seconds=3600)
        print("----nextTime:%s"%liveUtils.utcToLocal(nextCall))
        while not self.__stopped and liveUtils.utcnow() < nextCall:
            time.sleep(0.5)

    def stop(self):
        self.__stopped = True

    def stopped(self):
        return self.__stopped

    def run(self):
        logger.debug("Thread started.")
        ret = True
        while not self.__stopped:
            if ret:
                self.__wait()
            if not self.__stopped:
                ret = False
                try:
                    ret = self.doCall()
                except Exception, e:
                    logger.critical("Unhandled exception", exc_info=e)
        logger.debug("Thread finished.")

    # Must return a non-naive datetime.
    def getNextCallDateTime(self):
        raise NotImplementedError()

    def doCall(self):
        raise NotImplementedError()


class GetBarThread(PollingThread):

    # Events
    ON_HISTORY_BARS = 0
    ON_BARS = 1

    def __init__(self, queue, identifiers, frequency, apiCallDelay):
        PollingThread.__init__(self)

        # Map frequency to precision and period.
        if frequency < bar.Frequency.MINUTE:
            raise Exception("Frequency must be greater than or equal to bar.Frequency.MINUTE")
        elif frequency < bar.Frequency.HOUR:
            self.__precision = "Minutes"
        elif frequency < bar.Frequency.DAY:
            self.__precision = "Hours"
        else:
            raise Exception("Frequency must be less than bar.Frequency.DAY")
        self.__period = frequency / bar.Frequency.MINUTE

        self.__queue = queue
        self.__identifiers = identifiers
        self.__frequency = frequency
        self.__nextBarClose = None
        # The delay between the bar's close and the API call.
        self.__apiCallDelay = apiCallDelay
        self.__updateNextBarClose()

    def __updateNextBarClose(self):
        self.__nextBarClose = resamplebase.build_range(liveUtils.utcnow(), self.__frequency).getEnding()

    def getNextCallDateTime(self):
        return self.__nextBarClose + self.__apiCallDelay

    def run(self):
        self.doGetHistory()
        super(GetBarThread, self).run()

    def doGetHistory(self):
        while not self.stopped():
            endTimestamp = dt.datetime_to_timestamp(self.__nextBarClose)
            self.__updateNextBarClose()
            dicts = {}

            try:
                for indentifier in self.__identifiers:
                    response = api.getKLineBar(indentifier, endTimestamp - self.__frequency*2, self.__period, 100)
                    if response is None:
                        raise Exception("getKLineBar return None!")
                    dicts[indentifier] = response
                break
            except:
                time.sleep(1)
                continue
            
        while not self.stopped():
            barDict = {}
            for indentifier in self.__identifiers:
                response = dicts[indentifier]
                if len(response) == 0:
                    break
                barDict[indentifier] = liveBar(response.pop(-1), self.__frequency)

            if len(barDict) == 0:
                break
            bars = bar.Bars(barDict)
            self.__queue.put((GetBarThread.ON_HISTORY_BARS, bars))
        
    def doCall(self):
        endTimestamp = dt.datetime_to_timestamp(self.__nextBarClose)
        barDict = {}

        for indentifier in self.__identifiers:
            try:
                response = api.getKLineBar(indentifier, endTimestamp - self.__frequency, self.__period)
                if response is None:
                    raise Exception("getKLineBar return None!")
                # logger.debug(response)
                barDict[indentifier] = liveBar(response[-1], self.__frequency)
            except:
                time.sleep(1)
                return False

        if len(barDict):
            bars = bar.Bars(barDict)
            self.__queue.put((GetBarThread.ON_BARS, bars))
            self.__updateNextBarClose()
            return True
        return False


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
        self.__isHistory = True
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
        return liveUtils.utcnow()

    def barsHaveAdjClose(self):
        return False

    def isHistory(self):
        return self.__isHistory

    def getNextBars(self):
        ret = None
        try:
            eventType, eventData = self.__queue.get(True, LiveFeed.QUEUE_TIMEOUT)
            if eventType in (GetBarThread.ON_BARS, GetBarThread.ON_HISTORY_BARS):
                self.__isHistory = eventType is GetBarThread.ON_HISTORY_BARS
                ret = eventData
            else:
                logger.error("Invalid event received: %s - %s" % (eventType, eventData))
        except Queue.Empty:
            pass
        return ret

