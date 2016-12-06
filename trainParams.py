import stockAnalyzer as sa
import dataCollector as dc
import dataAnalyzer as da
from yahoo_finance import Share

def train(stocks, paramList, derivativeStepRatio = 0.01, gradientStepRatio = 0.001):
    # Stock Metrics
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    # Gradient
    partialDerivatives = []
    # Load data.
    PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache = loadData(stocks)
    for x in range(20):
        # Get partial derivatives.
        partialDerivatives = getPartialDerivatives(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, paramList)
        # Step the param list in the right direction.
        paramList = gradientAscent(partialDerivatives, paramList, gradientStepRatio)
        newAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, paramList)
        print newAccuracy

def gradientAscent(partialDerivatives, paramList, gradientStepRatio):
    for index, param in enumerate(paramList):
        paramList[index] += partialDerivatives[index] * gradientStepRatio
    return paramList

def getPartialDerivatives(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, newParamList):
    baseAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, newParamList)
    partialDerivatives = [None] * len(newParamList)
    # Find the gradient by finding each dAS/dm
    for index, param in enumerate(newParamList):
        # Make a copy of the parameter list so we can modify to find partial derivatives.
        tempParamList = newParamList[:]
        # Change in metric = derivativeStepRatio * current metric value
        if (param != 0):
            dm = derivativeStepRatio * param
        else:
            dm = derivativeStepRatio
        # Compute the new metric to use
        tempParamList[index] += dm
        # Compute the new accuracy to find the delta
        newAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, tempParamList)
        # Compute delta
        dAS = newAccuracy - baseAccuracy
        partialDerivatives[index] = dAS / dm
    return partialDerivatives


def getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, initialParamList):
    # First, cache all stock data.
    predictedList = sa.growthProbabilityTraining(PECache, PEGCache, ShortCache, HistoricalCache, initialParamList)
    accuracyScore = da.getPredictionAccuracyScore(ActualChangeCache, predictedList)
    return accuracyScore

def loadData(stockList):
    PECache = []
    PEGCache = []
    ShortCache = []
    HistoricalCache = []
    ActualChangeCache = []
    for stock in stockList:
        PECache.append(dc.getPERatio(stock))
        PEGCache.append(dc.getPEGRatio(stock))
        ShortCache.append(dc.getShortRatio(stock))
        HistoricalCache.append(dc.getHistoricalData(stock))
        ActualChangeCache.append(dc.getActualChange(stock))
    return PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache

if __name__ == '__main__':
    derivativeStepRatio = 0.01
    gradientStepRatio = 0.005
    trainingSet = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM",
        "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE",
        "BAC"]
    initialParamList = [1, -1, 40, 0, 1, 0.15, 2, 2, 0, 1, 0.3, 1, -1, 5, 0, 1, 0.15, -7, 7, 7, 14, 5, 0.4]
    train(trainingSet, initialParamList, derivativeStepRatio, gradientStepRatio)
