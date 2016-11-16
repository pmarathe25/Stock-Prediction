from yahoo_finance import Share
import datetime

def growthProbability(stockName):
    stock = Share(stockName)

    PERatio = stock.get_price_earnings_ratio()
    weightPE = 0.1

    PEGRatio = stock.get_price_earnings_growth_ratio()
    weightPEG = 0.2

    ShortRatio = stock.get_short_ratio()
    weightShort = 0.1

    weightHistorical = 0.6

def getFiveDayHistory(stock):
    historicalDataGraph = []
    # Get a range of dates.
    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    dateDelta = datetime.timedelta(days = 8)
    startDate = (datetime.datetime.now() - dateDelta).strftime("%Y-%m-%d")
    # Get only the last 5 business days.
    historicalData = stock.get_historical(startDate, endDate)
    historicalData = historicalData[0:5]

    for i in range(5):
        # Create a graph where the x axis is 0 - 9 and the y axis is open and close prices
        historicalDataGraph += {2 * i, historicalData[i]['Open']}
        historicalDataGraph += {2 * i + 1, historicalData[i]['Close']}
