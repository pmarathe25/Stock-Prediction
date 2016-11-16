from yahoo_finance import Share
from scipy import stats
import datetime

def growthProbability(stockName):
    stock = Share(stockName)

    PERatio = stock.get_price_earnings_ratio()
    weightPE = 0.1

    PEGRatio = stock.get_price_earnings_growth_ratio()
    weightPEG = 0.2

    ShortRatio = stock.get_short_ratio()
    weightShort = 0.1

    historical = getFiveDaySlope(stockName)
    weightHistorical = 0.6

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
    historicalData = historicalData[0:5]
    # Create a graph where the x axis is 0 - 9 and the y axis is open and close prices
    for i in range(5):
        x += [2 * i, 2 * i + 1]
        y += [float(historicalData[i]['Open']), float(historicalData[i]['Close'])]
    print x
    print y
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope
