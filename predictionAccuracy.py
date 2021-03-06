import stockAnalyzer as sa
import parseStocks as ps
import dataCollector as dc
import dataAnalyzer as da
from yahoo_finance import Share

def getAccuracy():
    evaluationSet = ps.parseFile('nasdaqtraded.txt')[0::29]
    # evaluationSet = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM",
    #     "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE",
    #     "BAC"]
    PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache = dc.loadData(evaluationSet, 1, 6)
    analyzer = sa.stockAnalyzer('parameterList')
    predictedList = analyzer.growthProbabilityBatch(PECache, PEGCache, ShortCache, HistoricalCache)
    correctPercentage = da.getCorrectPercentage(ActualChangeCache, predictedList)
    return correctPercentage

if __name__ == '__main__':
    print getAccuracy()
