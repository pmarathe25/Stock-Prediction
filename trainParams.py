import stockAnalyzer as sa
import dataCollector as dc
import dataAnalyzer as da
import parseStocks as ps
from yahoo_finance import Share
import random

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
    PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache = dc.loadData(stocks, 1, 6)
    maxAccuracy = None
    bestParams = []
    # Create stock analyzer object
    analyzer = sa.stockAnalyzer(paramList)
    newAccuracy = 0
    oldAccuracy = 0
    # Train until kerboard interrupt. If the oldAccuracy is better than the newAccuracy
    # , save the best parameters found so far to a file and then randomize the parameterList.
    try:
        while True:
            # Save old accuracy.
            oldAccuracy = newAccuracy
            # Get partial derivatives.
            partialDerivatives = getPartialDerivatives(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, paramList, analyzer)
            # Step the param list in the right direction.
            paramList = gradientAscent(partialDerivatives, paramList, gradientStepRatio)
            # Compute new accuracy.
            newAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, paramList, analyzer)
            # Check max.
            if (maxAccuracy is None or newAccuracy > maxAccuracy):
                maxAccuracy = newAccuracy
                bestParams = paramList[:]
            # Save and shuffle when we are no longer improving.
            if (newAccuracy is not None and oldAccuracy is not None and newAccuracy <= oldAccuracy):
                print "Maximum accuracy score."
                print maxAccuracy
                # Save the best params so far.
                writeBestParams('parameterList', bestParams)
                # Randomize the parameterList
                paramList = randomizeParamList(bestParams)
                # Reset accuracy variables.
                newAccuracy = None
                oldAccuracy = None
    except KeyboardInterrupt:
        writeBestParams('parameterList', bestParams)
    print
    print "Most recent accuracy score."
    print newAccuracy
    print "Most recent parameter list."
    print paramList
    print "Maximum accuracy score."
    print maxAccuracy
    print "Best parameters."
    print bestParams

def randomizeParamList(bestParams):
    # Randomizes the param list based on the best params.
    random.seed()
    paramList = bestParams[:]
    for index, param in enumerate(paramList):
        paramList[index] = random.random() * (5 * param) - (2 * param)
    return paramList

def writeBestParams(filename, bestParams):
    print "Writing best parameters."
    with open(filename, 'w') as f:
        for param in bestParams:
            f.write(str(param) + ",")

def gradientAscent(partialDerivatives, paramList, gradientStepRatio):
    for index, param in enumerate(paramList):
        paramList[index] += partialDerivatives[index] * gradientStepRatio
    return paramList

def getPartialDerivatives(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, newParamList, analyzer):
    baseAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, newParamList, analyzer)
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
        newAccuracy = getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, tempParamList, analyzer)
        # Compute delta
        dAS = newAccuracy - baseAccuracy
        partialDerivatives[index] = dAS / dm
    return partialDerivatives

def getAccuracy(PECache, PEGCache, ShortCache, HistoricalCache, ActualChangeCache, initialParamList, analyzer):
    # First, cache all stock data.
    predictedList = analyzer.growthProbabilityTraining(PECache, PEGCache, ShortCache, HistoricalCache, initialParamList)
    accuracyScore = da.getPredictionAccuracyScore(ActualChangeCache, predictedList)
    return accuracyScore

if __name__ == '__main__':
    trainingSet = ps.parseFile('nasdaqtraded.txt')[0::39]
    # trainingSet = ["TSLA", "BRK.B", "HD", "FB", "AAPL", "ANET", "NVDA", "TXN", "CRM",
    #     "NKE", "LUV", "GE", "TWTR", "MEET", "GOOG", "MSFT", "AMD", "YHOO", "NE",
    #     "BAC"]
    initialParamList = [1, -1, 40, 0, 1, 0.15, 2, 2, 0, 1, 0.3, 1, -1, 5, 0, 1, 0.15, -7, 7, 7, 14, 5, 0.4]
    derivativeStepRatio = 0.025
    gradientStepRatio = 0.001
    train(trainingSet, initialParamList, derivativeStepRatio, gradientStepRatio)
