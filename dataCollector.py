from yahoo_finance import Share
from scipy import stats
import math
import datetime

def getPERatio(stockName):
    try:
        stock = Share(stockName)
        PERatio = stock.get_price_earnings_ratio()
    except:
        return None
    return PERatio

def getPEGRatio(stockName):
    try:
        stock = Share(stockName)
        PEGRatio = stock.get_price_earnings_growth_ratio()
    except:
        return None
    return PEGRatio

def getShortRatio(stockName):
    try:
        stock = Share(stockName)
        ShortRatio = stock.get_short_ratio()
    except:
        return None
    return ShortRatio

def getHistoricalData(stockName):
    try:
        stock = Share(stockName)
        historical = getFiveDayAvgPercentChange(stockName)
    except:
        return None
    return historical

def getActualChange(stockName):
    try:
        stock = Share(stockName)
        return stock.get_change()
    except:
        return None

def getFiveDayAvgPercentChange(stockName):
    try:
        stock = Share(stockName)
        x, y, date = getFiveDayHistoricalData(stockName)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        percentChange = float(slope) / float(stock.get_price()) * 100
        return percentChange
    except:
        return None

def getFiveDayAvgChange(stockName):
    try:
        stock = Share(stockName)
        percentChange = getFiveDayAvgPercentChange(stockName)
        return abs((percentChange / 100) * float(stock.get_price()))
    except:
        return None

def getFiveDayHistoricalData(stockName):
    try:
        # Initialize values.
        stock = Share(stockName)
        x = []
        y = []
        date = []
        # Get a range of dates.
        endDate = datetime.datetime.now().strftime("%Y-%m-%d")
        startDate = (datetime.datetime.now() - datetime.timedelta(days = 8)).strftime("%Y-%m-%d")
        # Get only the last 5 business days.
        historicalData = stock.get_historical(startDate, endDate)
        historicalData = historicalData[-5:]
        # Create a graph where the x axis is 0 - 4.5 and the y axis is open and close prices
        for i in range(5):
            x += [5.5 - i, 5.5 - (i + float(1) / 2)]
            y += [float(historicalData[i]['Open']), float(historicalData[i]['Close'])]
            date += [historicalData[i]['Date']]
        x += [0.5, 0]
        y = [float(stock.get_price()), float(stock.get_price())] + y
        return x, y, date
    except:
        return None, None, None

def loadData(stockList):
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    for index, stock in enumerate(stockList):
        sys.stdout.write("Progress: %d / %d stocks loaded. \r" % (index, len(stockList)))
        sys.stdout.flush()
        PECache.append(dc.getPERatio(stock))
        PEGCache.append(dc.getPEGRatio(stock))
        ShortCache.append(dc.getShortRatio(stock))
        HistoricalCache.append(dc.getHistoricalData(stock))
        ActualChangeCache.append(dc.getActualChange(stock))
    return PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache
