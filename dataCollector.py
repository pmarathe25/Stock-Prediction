from yahoo_finance import Share
from scipy import stats
import math
import datetime

def getPERatio(stockName, weight = 0.15):
    weightPE = 0.01
    stock = Share(stockName)
    PERatio = stock.get_price_earnings_ratio()
    if (PERatio is not None):
        weightPE = weight
    return PERatio, weightPE

def getPEGRatio(stockName, weight = 0.3):
    weightPEG = 0.01
    stock = Share(stockName)
    PEGRatio = stock.get_price_earnings_growth_ratio()
    if (PEGRatio is not None):
        weightPEG = weight
    return PEGRatio, weightPEG

def getShortRatio(stockName, weight = 0.15):
    weightShort = 0.01
    stock = Share(stockName)
    ShortRatio = stock.get_short_ratio()
    if (ShortRatio is not None):
        weightShort = weight
    return ShortRatio, weightShort

def getHistoricalData(stockName, weight = 0.4):
    weightHistorical = 0.01
    stock = Share(stockName)
    try:
        historical = getFiveDayAvgPercentChange(stockName)
        weightHistorical = weight
    except:
        return None, weightHistorical
    return historical, weightHistorical

def getFiveDayAvgPercentChange(stockName):
    stock = Share(stockName)
    x, y, date = getFiveDayHistoricalData(stockName)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    percentChange = float(slope) / float(stock.get_price()) * 100
    return percentChange

def getFiveDayAvgChange(stockName):
    stock = Share(stockName)
    percentChange = getFiveDayAvgPercentChange(stockName)
    return abs((percentChange / 100) * float(stock.get_price()))

def getFiveDayHistoricalData(stockName):
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
