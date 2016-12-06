import stockAnalyzer
import dataCollector as dc
import dataAnalyzer as da
from yahoo_finance import Share

def train(initialParamList):
    stocks = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM",
        "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE",
        "BAC"]
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    # First, cache all stock data.
    PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache = loadData(stocks)

def loadData(stockList):
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    for (stock in stockList):
        PECache += dc.getPERatio(stock)
        PEGCache += dc.getPEGRatio(stock)
        ShortCache += dc.getShortRatio(stock)
        HistoricalCache += dc.getHistoricalData(stock)
        ActualChangeCache = dc.getActualChange(stock)
    return PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache

if __name__ == '__main__':
    initialParamList = [1, -1, 40, 0, 1, 0.15, 2, 2, 0, 1, 0.3, 1, -1, 5, 0, 1, 0.15, -7, 7, 7, 14, 5, 0.4]
    train(initialParamList)
