import stockAnalyzer
import dataCollector as dc
import dataAnalyzer as da
from yahoo_finance import Share

def train():
    stocks = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM",
        "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE",
        "BAC"]
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    # First, cache all stock data.
    PECache, PEGCache, ShortCache, HistoricalCache = loadData(stocks)

def loadData(stockList):
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    for (stock in stockList):
        PECache += dc.getPERatio(stock)
        PEGCache += dc.getPEGRatio(stock)
        ShortCache += dc.getShortRatio(stock)
        HistoricalCache += dc.getHistoricalData(stock)
    return PECache, PEGCache, ShortCache, HistoricalCache



if __name__ == '__main__':
    train()
