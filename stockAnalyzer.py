from yahoo_finance import Share
from scipy import stats
import math
import datetime

def growthProbability(stockName):
    stock = Share(stockName)

    PERatio = stock.get_price_earnings_ratio()
    #  Scale PE Ratio
    PERatio = 1 - 1 / math.exp(float(PERatio) / 40)
    weightPE = 0.15

    PEGRatio = stock.get_price_earnings_growth_ratio()
    # Scale PEG Ratio
    PEGRatio = (4 - float(PEGRatio)) / 4
    weightPEG = 0.3

    ShortRatio = stock.get_short_ratio()
    # Scale Short Ratio
    ShortRatio = 1 - 1 / math.exp(float(ShortRatio) / 5)
    weightShort = 0.15

    historical = getFiveDaySlope(stockName)
    # Scale 5 day slope
    historical = float(historical) / float(stock.get_price()) * 100
    if (historical > 5.0):
        historical = 5.0
    historical = math.sin(historical)
    weightHistorical = 0.4

    return PERatio * weightPE + PEGRatio * weightPEG + ShortRatio * weightShort + historical * weightHistorical

def getFiveDaySlope(stockName):
    # Initialize values.
    stock = Share(stockName)
    x = []
    y = []
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
    x += [0.5, 0]
    y = [float(stock.get_price()), float(stock.get_price())] + y
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope
