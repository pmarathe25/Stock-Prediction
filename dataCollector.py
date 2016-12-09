from yahoo_finance import Share
from scipy import stats
import sys
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

def getHistoricalData(stockName, startDay, endDay):
    try:
        stock = Share(stockName)
        historical = getWeekAvgPercentChange(stockName, startDay, endDay)
    except:
        return None
    return historical

def getActualChange(stockName):
    try:
        stock = Share(stockName)
        return stock.get_change()
    except:
        return None

def getWeekAvgPercentChange(stockName, startDay, endDay):
    try:
        stock = Share(stockName)
        x, y, date = getWeekHistoricalData(stockName, startDay, endDay)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        percentChange = float(slope) / float(stock.get_price()) * 100
        return percentChange
    except:
        return None

def getWeekAvgChange(stockName, startDay, endDay):
    try:
        stock = Share(stockName)
        percentChange = getWeekAvgPercentChange(stockName, startDay, endDay)
        return abs((percentChange / 100) * float(stock.get_price()))
    except:
        return None

def getWeekHistoricalData(stockName, startDay, endDay):
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
        historicalData = historicalData[startDay:endDay]
        # Create a graph where the x axis is 0 - 4.5 and the y axis is open and close prices
        numDays = endDay - startDay
        for i in range(numDays):
            x += [(numDays + 0.5) - i, (numDays + 0.5) - (i + float(1) / 2)]
            y += [float(historicalData[i]['Open']), float(historicalData[i]['Close'])]
            date += [historicalData[i]['Date']]
        x += [0.5, 0]
        y = [float(stock.get_price()), float(stock.get_price())] + y
        return x, y, date
    except:
        return None, None, None

def loadData(stockList, startDay, endDay):
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    for index, stock in enumerate(stockList):
        sys.stdout.write("Progress: %d / %d stocks loaded. \r" % (index, len(stockList)))
        sys.stdout.flush()
        PECache.append(getPERatio(stock))
        PEGCache.append(getPEGRatio(stock))
        ShortCache.append(getShortRatio(stock))
        HistoricalCache.append(getHistoricalData(stock, startDay, endDay))
        ActualChangeCache.append(getActualChange(stock))
    print
    return PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache
