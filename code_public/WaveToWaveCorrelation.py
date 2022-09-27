from DataReader import DataReader
import scipy.stats
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

class MetricWavesData:
    def __init__(self, name):
        self._name = name
        self._waveData = dict()
        self._classInWaves = dict()


    def getClassDataMap(self, classID):
        d = None
        if classID in self._classInWaves.keys():
            d = self._classInWaves[classID]
        else:
            d = dict()
            self._classInWaves[classID] = d
        return d

    def addWaveToClass(self, waveID, classID, data):
        d = self.getClassDataMap(classID)
        d[waveID] = data

    def getDataOfClassInWave(self, classID, waveID):
        d = self.getClassDataMap(classID)
        if waveID in d.keys():
            return d[waveID]
        return None


    def getAvailableDataListOfWave(self, waveID):
        l = None
        if waveID in self._waveData.keys():
            l = self._waveData[waveID]
        else:
            l = list()
            self._waveData[waveID] = l
        return l

    def addDataToWave(self, waveID, classID, data):
        l = self.getAvailableDataListOfWave(waveID)
        if waveID in self._waveData.keys():
            l = self._waveData[waveID]
        else:
            l = list()
            self._waveData[waveID] = l
        l.append((classID, data))
        self.addWaveToClass(waveID, classID, data)


class WaveSummaryStatistics:
    def __init__(self, mean, median, variance):
        self._mean = mean
        self._median = median
        self._variance = variance
        
    def mean(self):
        return self._mean
    
    def median(self):
        return self._median
    
    def variance(self):
        return self._variance

class MetricsWaveToWaveCorrelationResults:
    def __init__(self, name):
        self._name = name
        self._waveToWaveCorrelationDict = dict()
        self._waveSummaryStatistics = dict()

    def name(self):
        return self._name

    def WtWCorrelationList(self, fromWave, toWave):
        key = str(fromWave) + "," + str(toWave)
        l = None
        if key in self._waveToWaveCorrelationDict.keys():
            l = self._waveToWaveCorrelationDict[key]
        else:
            l = list()
            self._waveToWaveCorrelationDict[key] = l
        return l
    
    def getWaveToWaveCorrelationDict(self):
        return self._waveToWaveCorrelationDict
    
    def getWaveSummaryStatisticsDict(self):
        return self._waveSummaryStatistics

class WaveToWaveCorrelation(DataReader):
    def __init__(self, name,  resultsFolderStructure, resultsDir, metrics, metricNames):
        self._name = name
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._metrics = metrics
        self._metricNames = metricNames
        self._metricData = dict()
        self._maxTurnIndex = 0
        self._metricResults = dict()
        self._minVariance = 1e10
        self._maxVariance = -1e10



    def getMetricResults(self, metricName):
        metricResult = None
        if metricName in self._metricResults.keys():
            metricResult = self._metricResults[metricName]
        else:
            metricResult = MetricsWaveToWaveCorrelationResults(metricName)
            self._metricResults[metricName] = metricResult
        return metricResult

    def addMetricDataToWave(self, metricKey, metricData, waveID, classID):
        metricWavesData = None
        if metricKey in self._metricData.keys():
            metricWavesData = self._metricData[metricKey]
        else:
            metricWavesData = MetricWavesData(metricKey)
            self._metricData[metricKey] = metricWavesData
        metricWavesData.addDataToWave(waveID, classID, metricData)

    def readTurn(self, turn):
        for metric in self._metrics:
            metricKey = metric.unique_name()
            if turn.hasKey(metricKey) == False:
                continue
            metricData = turn.get(metricKey)
            classID = turn.parent().id()
            self.addMetricDataToWave(metricKey, metricData, turn.index(), classID)
            if turn.index() > self._maxTurnIndex:
                self._maxTurnIndex = turn.index()


    def computeCorrelation(self, dataObjCurrent, dataObjNext):
        pass

    def computeForMetric(self, metricResultObj):
        metricName = metricResultObj.name()
        waveIDs = range(1, self._maxTurnIndex)
        metricData = self._metricData[metricName]
        for waveID in waveIDs:
            nextWaveID = waveID + 1
            dataListOfCurrentWave = metricData.getAvailableDataListOfWave(waveID)
            wtwCorrelationList = metricResultObj.WtWCorrelationList(waveID, nextWaveID)
            for dataInCurrentWave in dataListOfCurrentWave:
                classID = dataInCurrentWave[0]
                dataObjCurrent = dataInCurrentWave[1]
                dataObjNext = metricData.getDataOfClassInWave(classID, nextWaveID)
                if dataObjNext != None:
                    corr = self.computeCorrelation(dataObjCurrent, dataObjNext)
                    if not np.isnan(corr):
                        wtwCorrelationList.append((classID, corr))




    def compute(self):
        for metric in self._metrics:
            metricKey = metric.unique_name()
            metricResultObj = self.getMetricResults(metricKey)
            self.computeForMetric(metricResultObj)


    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self.compute()
        self.postProcess()
    
    def processMetricResults(self, metricResultsObj, resultsFile):
        wtwCorrelationsDict = metricResultsObj.getWaveToWaveCorrelationDict()
        n = len(wtwCorrelationsDict)
        r = range(1, n + 1)
        correlationValuesDict = dict()
        for waveIndex in r:
            resultsFile.write("**********" + str(waveIndex) + "->" + str(waveIndex + 1) + "**********\n")
            correlationsList = metricResultsObj.WtWCorrelationList(waveIndex, waveIndex + 1)
            correlationValues = list()
            for classCorrelationPair in correlationsList:
                resultsFile.write(str(classCorrelationPair[0]) + ": " + str(classCorrelationPair[1]) + "\n")
                correlationValues.append(classCorrelationPair[1])
            correlationValuesDict[waveIndex] = correlationValues
        return correlationValuesDict
            
    def buildSummaryStatistic(self, correlationValuesDict, metricResultsObj, resultsFile):
        waveSummaryStatisticsDict = metricResultsObj.getWaveSummaryStatisticsDict()
        for item in correlationValuesDict.items():
            waveIndex = item[0]
            correlations = item[1]
            mean = np.mean(correlations)
            median = np.median(correlations)
            variance = np.var(correlations)
            if variance > self._maxVariance:
                self._maxVariance = variance
            if variance < self._minVariance:
                self._minVariance = variance
            s = str(waveIndex) + " -> " + str(waveIndex + 1) + ": "
            s = s + "mean = " + str(mean) + " median = " + str(median)
            s = s + " variance = " + str(variance) + "\n"
            waveSummaryStatistics = WaveSummaryStatistics(mean, median, variance)
            waveSummaryStatisticsDict[waveIndex] = waveSummaryStatistics
            resultsFile.write(s)
            
    
    
    def createHeatMap(self):
        nMetrics = len(self._metricResults)
        nWaweStatistics = None
        for item in self._metricResults.values():
            waveSummaryStatisticsDict = item.getWaveSummaryStatisticsDict()
            if nWaweStatistics == None:
                nWaweStatistics = len(waveSummaryStatisticsDict)
            else:
                if len(waveSummaryStatisticsDict) != nWaweStatistics:
                    raise Exception("Invalid summary statistic number!")
        
        mx = np.empty((nMetrics, nWaweStatistics))
        mx[:] = np.nan
        
        rngMetrics = range(nMetrics)
        rngWaves = range(nWaweStatistics)
        for i in rngMetrics:
            metric = self._metrics[i]
            metricName = metric.metricKey = metric.unique_name()
            resultsObject = self._metricResults[metricName]
            waveSummaryStatisticsDict = resultsObject.getWaveSummaryStatisticsDict()
            for j in rngWaves:
                waveID = j + 1
                summaryStatistics = waveSummaryStatisticsDict[waveID]
                mean = summaryStatistics.mean()
                mx[(i,j)] = mean
        cmap = sb.diverging_palette(500, 10, as_cmap=True)
        x_labels = []
        for i in rngWaves:
            x_labels.append(str(i + 1))
        hm = sb.heatmap(mx, cmap=cmap, annot=True,  xticklabels = x_labels, yticklabels = self._metricNames, vmax= 1.0, cbar = True)
        figure = hm.get_figure()
        plt.xlabel("waves", fontweight='normal', fontsize=12)
        #plt.ylabel("centrality measures", fontweight='normal', fontsize=12)
        targetFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + "WaveToWaveCorrelations.png"
        figure.savefig(targetFilePath)
        plt.close()
            
    def postProcess(self):
        for item in self._metricResults.items():
            metric_name = item[0]
            resultsObj = item[1]
            filePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + metric_name + "_" + self._name +"_wtw.txt"
            f = open(filePath, "w")
            correlationValuesDict = self.processMetricResults(resultsObj, f)
            self.buildSummaryStatistic(correlationValuesDict, resultsObj, f)
            f.close()
        print("Min variance: " + str(self._minVariance) + " max variance: " + str(self._maxVariance) + "\n")
        self.createHeatMap()

class KendallTauWaveToWaveCorrelation(WaveToWaveCorrelation):

    def computeCorrelation(self, dataObjCurrent, dataObjNext):
        currentIDList = dataObjCurrent.idsList()
        nextIDList = dataObjNext.idsList()
        common_id_set = set(currentIDList) & set(nextIDList)
        currentIDtoValue = dataObjCurrent.idToValueDict()
        nextIDtoValue = dataObjNext.idToValueDict()
        current_values = []
        next_values = []
        for student_id in common_id_set:
            current_values.append(currentIDtoValue[student_id])
            next_values.append(nextIDtoValue[student_id])
        tau, p_value = scipy.stats.kendalltau(current_values, next_values)
        if (not np.isnan(tau)) and (tau < 0.0):
            tau = 0.0 

        return tau
