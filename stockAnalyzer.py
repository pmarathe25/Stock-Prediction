import dataCollector as dc
import dataAnalyzer as da

def growthProbability(stockName, paramList):
    PERatio = dc.getPERatio(stockName)
    PEGRatio = dc.getPEGRatio(stockName)
    ShortRatio = dc.getShortRatio(stockName)
    HistoricalData = dc.getHistoricalData(stockName)

    PERatio, weightPE = da.processPERatio(PERatio)
    PEGRatio, weightPEG = da.processPEGRatio(PEGRatio)
    ShortRatio, weightShort = da.processShortRatio(ShortRatio)
    HistoricalData, weightHistorical = da.processHistorical(HistoricalData)

    probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio * weightShort + HistoricalData * weightHistorical) / (weightPE + weightPEG + weightShort + weightHistorical)
    return probability

def growthProbabilityTraining(PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList, paramList):
    # Accepts cached metric lists.

    return probabilityList
