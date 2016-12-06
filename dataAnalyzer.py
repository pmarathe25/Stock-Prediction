from yahoo_finance import Share
from scipy import stats
import math
import datetime
import helpers

def processPERatio(PERatio, paramList = [1, -1, 40, 0, 1, 0.15]):
    weightPE = 0.01
    #  Scale PE Ratio
    if (PERatio is not None):
        PERatio = paramList[0] + paramList[1] / math.exp(float(PERatio) / paramList[2])
        PERatio = helpers.clamp(PERatio, paramList[3], paramList[4])
        weightPE = paramList[5]
    else:
        print "Could not retrieve PE ratio."
        PERatio = 0
    return PERatio, weightPE

def processPEGRatio(PEGRatio, paramList = [2, 2, 0, 1, 0.3]):
    weightPEG = 0.01
    # Scale PEG Ratio
    if (PEGRatio is not None):
        PEGRatio = (paramList[0] - float(PEGRatio)) / paramList[1]
        # Clamp PEG Ratio
        PEGRatio = helpers.clamp(PEGRatio, paramList[2], paramList[3])
        weightPEG = paramList[4]
    else:
        print "Could not retrieve PEG ratio."
        PEGRatio = 0
    return PEGRatio, weightPEG

def processShortRatio(ShortRatio, paramList = [1, -1, 5, 0, 1, 0.15]):
    weightShort = 0.01
    # Scale Short Ratio
    if (ShortRatio is not None):
        ShortRatio = paramList[0] + paramList[1] / math.exp(float(ShortRatio) / paramList[2])
        ShortRatio = helpers.clamp(ShortRatio, paramList[3], paramList[4])
        weightShort = paramList[5]
    else:
        print "Could not retrieve short ratio."
        ShortRatio = 0
    return ShortRatio, weightShort

def processHistorical(historical, paramList = [-7, 7, 7, 14, 5, 0.4]):
    weightHistorical = 0.01
    # Process historical data
    if (historical is not None):
        # Clamp historical price change between -4% and +4%
        historical = helpers.clamp(historical, paramList[0], paramList[1])
        historical = (historical + paramList[2]) / paramList[3] + math.sin(historical / paramList[4])
        weightHistorical = paramList[5]
    else:
        print "Could not retrieve historical data."
        historical = 0
    return historical, weightHistorical

def getCorrectPercentage(actualChangeList, predictedChangeList):
    for actual, predicted in zip(actualChangeList, predictedChangeList):
        if (actual is not None):
            actual = float(actual)
            if (predicted >= .5 and actual >= 0):
                correct += 1
            elif (predicted <= .5 and actual <= 0):
                correct += 1
            total += 1
    return correct / total

def getPredictionAccuracyScore(actualChangeList, predictedChangeList):
    for actual, predicted in zip(actualChangeList, predictedChangeList):
        if (actual is not None):
            actual = float(actual)
            if (predicted >= .5 and actual >= 0):
                predictionScore += predicted
            elif (predicted <= .5 and actual <= 0):
                predictionScore += (1 - predicted)
    return predictionScore
