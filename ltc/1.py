from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 10000)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = {}
        self.__sma[smaPeriod] = ma.SMA(self.__prices, smaPeriod)
        self.__sma[10] = ma.SMA(self.__prices, 10)
        self.__sma[30] = ma.SMA(self.__prices, 30)

    def getSMA(self, period):
        return self.__sma[period]
    
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[30][-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__sma[10], self.__sma[30]) > 0:
                self.__position = self.enterLong(self.__instrument, 50, True)
        # Check if we have to exit the position.
#        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma[10]) > 0:
        elif not self.__position.exitActive() and cross.cross_below(self.__sma[10], self.__sma[30]) > 0:
            self.__position.exitMarket()


def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
    feed = GenericBarFeed(Frequency.DAY, None, None)
    feed.addBarsFromCSV("orcl", "2000.csv")

    # Evaluate the strategy with the feed.
    myStrategy = MyStrategy(feed, "orcl", smaPeriod)
    
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    

    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot("orcl").addDataSeries("SMA%d"%smaPeriod, myStrategy.getSMA(smaPeriod))
    plt.getInstrumentSubplot("orcl").addDataSeries("SMA10", myStrategy.getSMA(10))
    plt.getInstrumentSubplot("orcl").addDataSeries("SMA30", myStrategy.getSMA(30))
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())
    
    
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()
#    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

    # Plot the strategy.
    plt.plot()

run_strategy(60)















