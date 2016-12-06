from yahoo_finance import Share
from scipy import stats
import math
import datetime
import helpers

def processPERatio(PERatio):
    #  Scale PE Ratio
    if (PERatio is not None):
        PERatio = 1 - 1 / math.exp(float(PERatio) / 40)
        PERatio = helpers.clamp(PERatio, 0, 1)
    else:
        print "Could not retrieve PE ratio."
        PERatio = 0
    return PERatio

def processPEGRatio(PEGRatio):
    # Scale PEG Ratio
    if (PEGRatio is not None):
        PEGRatio = (2 - float(PEGRatio)) / 2
        # Clamp PEG Ratio
        PEGRatio = helpers.clamp(PEGRatio, 0, 1)
    else:
        print "Could not retrieve PEG ratio."
        PEGRatio = 0
    return PEGRatio

def processShortRatio(ShortRatio):
    # Scale Short Ratio
    if (ShortRatio is not None):
        ShortRatio = 1 - 1 / math.exp(float(ShortRatio) / 5)
        ShortRatio = helpers.clamp(ShortRatio, 0, 1)
    else:
        print "Could not retrieve short ratio."
        ShortRatio = 0
    return ShortRatio

def processHistorical(historical):
    # Process historical data
    if (historical is not None):
        # Clamp historical price change between -4% and +4%
        historical = helpers.clamp(historical, -7, 7)
        historical = (historical + 7) / 14 + math.sin(historical / 5)
    else:
        print "Could not retrieve historical data."
        historical = 0
    return historical
