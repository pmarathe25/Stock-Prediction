import stockAnalyzer
from yahoo_finance import Share

def getAccuracy():
    stocks = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM", "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE", "BAC"]
    total = 0
    correct = 0
    for stock in stocks:
        print stock
        stockActual = Share(stock)
        actual = stockActual.get_change()
        probability = stockAnalyzer.growthProbability(stock)
        if (actual is not None):
            print float(actual)
            print probability
            actual = float(actual)
            if (probability >= .5 and actual >= 0):
                correct += 1
            elif (probability <= .5 and actual <= 0):
                correct += 1
            total += 1
    print "Correct"
    print correct
    print "Total"
    print total
    return correct / total

if __name__ == '__main__':
    getAccuracy()
