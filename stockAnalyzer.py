import dataCollector as dc
import dataAnalyzer as da

class stockAnalyzer:
    paramList = []
    def __init__(self, filename):
        if type(filename) == type([]):
            print "Using provided parameter list."
            self.paramList = filename[:]
        else:
            self.paramList = self.readParams(filename)

    def growthProbability(self, stockName):
        PERatio = dc.getPERatio(stockName)
        PEGRatio = dc.getPEGRatio(stockName)
        ShortRatio = dc.getShortRatio(stockName)
        HistoricalData = dc.getHistoricalData(stockName)

        PERatio, weightPE = da.processPERatio(PERatio, self.paramList[0:6])
        PEGRatio, weightPEG = da.processPEGRatio(PEGRatio, self.paramList[6:11])
        ShortRatio, weightShort = da.processShortRatio(ShortRatio, self.paramList[11:17])
        HistoricalData, weightHistorical = da.processHistorical(HistoricalData, self.paramList[17:])

        probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio
            * weightShort + HistoricalData * weightHistorical) / (weightPE
            + weightPEG + weightShort + weightHistorical)
        return probability

    def growthProbabilityTraining(self, PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList, testParams):
        probabilityList = []
        # Accepts cached metric lists.
        for PERatio, PEGRatio, ShortRatio, HistoricalData in zip (PERatioList, PEGRatioList, ShortRatioList, HistoricalDataList):
            PERatio, weightPE = da.processPERatio(PERatio, testParams[0:6])
            PEGRatio, weightPEG = da.processPEGRatio(PEGRatio, testParams[6:11])
            ShortRatio, weightShort = da.processShortRatio(ShortRatio, testParams[11:17])
            HistoricalData, weightHistorical = da.processHistorical(HistoricalData, testParams[17:])
            probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio
                * weightShort + HistoricalData * weightHistorical) / (weightPE
                + weightPEG + weightShort + weightHistorical)
            probabilityList.append(probability)
        return probabilityList

    def readParams(self, filename):
        params = []
        with open(filename) as f:
            line = f.readline()
            for elem in line.split(','):
                if elem is not None and elem != "":
                    params.append(float(elem))
        return params
