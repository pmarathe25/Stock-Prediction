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

    probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio
        * weightShort + HistoricalData * weightHistorical) / (weightPE
        + weightPEG + weightShort + weightHistorical)
    return probability

def growthProbabilityTraining(PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList, paramList):
    probabilityList = []
    # Accepts cached metric lists.
    for PERatio, PEGRatio, ShortRatio, HistoricalData in zip (PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList):
        PERatio, weightPE = da.processPERatio(PERatio, paramList[0:6])
        PEGRatio, weightPEG = da.processPEGRatio(PEGRatio, paramList[6:11])
        ShortRatio, weightShort = da.processShortRatio(ShortRatio, paramList[11:17])
        HistoricalData, weightHistorical = da.processHistorical(HistoricalData, paramList[17:])
        probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio
            * weightShort + HistoricalData * weightHistorical) / (weightPE
            + weightPEG + weightShort + weightHistorical)
        probabilityList.append(probability)
    return probabilityList
