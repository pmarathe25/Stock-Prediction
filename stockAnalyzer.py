import dataCollector as dc
import dataAnalyzer as da

def growthProbability(stockName, paramList):
    PERatio, weightPE = dc.getPERatio(stockName)
    PEGRatio, weightPEG = dc.getPEGRatio(stockName)
    ShortRatio, weightShort = dc.getShortRatio(stockName)
    HistoricalData, weightHistorical = dc.getHistoricalData(stockName)

    PERatio = da.processPERatio(PERatio)
    PEGRatio = da.processPEGRatio(PEGRatio)
    ShortRatio = da.processShortRatio(ShortRatio)
    HistoricalData = da.processHistorical(HistoricalData)

    probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio * weightShort + HistoricalData * weightHistorical) / (weightPE + weightPEG + weightShort + weightHistorical)
    return probability

def growthProbability(PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList, paramList):
    
    return probability
