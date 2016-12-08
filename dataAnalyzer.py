from yahoo_finance import Share
from scipy import stats
import math
import datetime
import helpers

def processPERatio(PERatio, paramList = [1, -1, 40, 0, 1, 0.15]):
    #  Scale PE Ratio
    try:
        PERatio = paramList[0] + float(PERatio) * paramList[1] + math.exp(float(PERatio)) * paramList[2]
        PERatio = helpers.clamp(PERatio, paramList[3], paramList[4])
        weightPE = paramList[5]
    except:
        PERatio = 0
        weightPE = 0.01
    return PERatio, weightPE

def processPEGRatio(PEGRatio, paramList = [2, 2, 0, 1, 0.3]):
    # Scale PEG Ratio
    try:
        PEGRatio = (paramList[0] - float(PEGRatio)) * paramList[1]
        # Clamp PEG Ratio
        PEGRatio = helpers.clamp(PEGRatio, paramList[2], paramList[3])
        weightPEG = paramList[4]
    except:
        PEGRatio = 0
        weightPEG = 0.01
    return PEGRatio, weightPEG

def processShortRatio(ShortRatio, paramList = [1, -1, 5, 0, 1, 0.15]):
    # Scale Short Ratio
    try:
        ShortRatio = paramList[0] + float(ShortRatio) * paramList[1] + math.exp(float(ShortRatio)) * paramList[2]
        ShortRatio = helpers.clamp(ShortRatio, paramList[3], paramList[4])
        weightShort = paramList[5]
    except:
        ShortRatio = 0
        weightShort = 0.01
    return ShortRatio, weightShort

def processHistorical(historical, paramList = [-7, 7, 7, 14, 5, 0.4]):
    # Process historical data
    try:
        # Clamp historical price change between -4% and +4%
        historical = helpers.clamp(historical, paramList[0], paramList[1])
        historical = paramList[2] + historical * paramList[3] + math.sin(historical) * paramList[4]
        weightHistorical = paramList[5]
    except:
        historical = 0
        weightHistorical = 0.01
    return historical, weightHistorical

def getCorrectPercentage(actualChangeList, predictedChangeList):
    total = 0.0
    correct = 0.0
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
    predictionScore = 0
    for actual, predicted in zip(actualChangeList, predictedChangeList):
        if (actual is not None):
            actual = float(actual)
            # Penalize out of range predictions heavily.
            if (predicted > 1 or predicted < 0):
                predictionScore -= 1
            elif (actual > 0):
                predictionScore += (predicted - 0.5)
            elif (actual <= 0):
                predictionScore += (0.5 - predicted)
    return predictionScore
