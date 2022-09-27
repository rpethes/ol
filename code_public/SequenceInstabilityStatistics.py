from TemporalStatBuilder import TemporalStatBuilder
from TemporalDataBuilder import FOLLOWER_TEMPORAL_DATA_KEY
from TemporalDataBuilder import FRIEND_TEMPORAL_DATA_KEY
from TemporalDataBuilder import AGGR_TEMPORAL_DATA_KEY
import numpy as np
import matplotlib.pyplot as plt

class SequenceInstabilityStatisticsData:
    def __init__(self):
        self._values = []
        self._valueDict = {}
        
    def values(self):
        return self._values
    
    def valueDict(self):
        return self._valueDict


class SequenceInstabilityStatistics(TemporalStatBuilder):
    
    class Stats:
        def __init__(self):
            self.sample_size = None
            self.mean = None
            self.median = None
            self.perc25 = None
            self.perc75 = None
            self.var = None
            self.min_value = None
            self.max_value = None
            self.hist = None 
            self.bins = None
            self.histogramFilePath = None
            self.stat_file = None 
            
    def __init__(self, name, target_user_data_key, prefix, resultsFolderStructure, resultsDir):
        TemporalStatBuilder.__init__(self, name, target_user_data_key, prefix, resultsFolderStructure, resultsDir)
        self._sequenceLengthDataMap = dict()
        self._stats = dict()
    
    def getStatsOfSequenceLength(self, sequenceLen_):
        return self._stats[sequenceLen_]
    
    def processData(self, data, schoolClass):
        sequenceLength = data.getSequenceLen()
        sequenceInstabilityStatisticsData = self._sequenceLengthDataMap.get(sequenceLength, None)
        if sequenceInstabilityStatisticsData == None:
            sequenceInstabilityStatisticsData = SequenceInstabilityStatisticsData()
            self._sequenceLengthDataMap[sequenceLength] = sequenceInstabilityStatisticsData
        
        value = data.getValue()
        sequenceInstabilityStatisticsData._values.append(value)
        if value in sequenceInstabilityStatisticsData._valueDict.keys():
            valueList = sequenceInstabilityStatisticsData._valueDict[value]
        else:
            valueList = []
            sequenceInstabilityStatisticsData._valueDict[value] = valueList 
        valueList.append(schoolClass.id())
    
    def buildStatistics(self, schools):
        for sequenceLength, data in self._sequenceLengthDataMap.items():
            stat = self.buildStat(sequenceLength, data)
            self._stats[sequenceLength] = stat
            
    def buildStat(self, sequenceLength, data):
        statsObj = self.Stats()
        statsObj.sample_size = len(data._values)
        statsObj.mean = np.mean(data._values)
        statsObj.median = np.median(data._values)
        statsObj.perc25 = np.percentile(data._values, 25)
        statsObj.perc75 = np.percentile(data._values, 75)
        statsObj.var = np.var(data._values)
        statsObj.min_value = np.min(data._values)
        statsObj.max_value = np.max(data._values)
        statsObj.hist, statsObj.bins = np.histogram(data._values, bins = 10, range = (statsObj.min_value, statsObj.max_value), density = False)
        base_path = self._resultsDir + self._prefix + self._name + "_" + str(sequenceLength)
        statsObj.histogramFilePath = base_path + "_histogram.png"
        plt.hist(data._values, bins = statsObj.bins) 
        plt.savefig(statsObj.histogramFilePath)
        plt.close()
        statsObj.stat_file = base_path + "_stats.txt"
        f = open(statsObj.stat_file, "w")
        f.write("sample size = " + str(statsObj.sample_size) + "\n")
        f.write("mean = " + str(statsObj.mean) + "\n")
        f.write("median = " + str(statsObj.median) + "\n")
        f.write("percentile 25 = " + str(statsObj.perc25) + "\n")
        f.write("percentile 75 = " + str(statsObj.perc75) + "\n")
        f.write("variance = " + str(statsObj.var) + "\n")
        f.write("min = " + str(statsObj.min_value) + "\n")
        f.write("max = " + str(statsObj.max_value) + "\n")
        f.write("bins = " + str(statsObj.bins) + "\n")
        f.write("hist = " + str(statsObj.hist) + "\n")
        
        
        values = list(data._valueDict.keys())
        values.sort(key = (lambda x : abs(x - statsObj.mean)))
        n = min(10, len(values))
        for i in range(n):
            v = values[i]
            f.write("distance = " + str(abs(v - statsObj.mean)) + "schoool class: ")
            l = data._valueDict[v]
            for schoolClassID in l: 
                f.write(str(schoolClassID) + " ")
            f.write("\n")
        f.close()
        return statsObj
        
class SequenceInstabilityStatisticsFollower(SequenceInstabilityStatistics):
    def __init__(self, name, resultsFolderStructure, resultsDir):
        SequenceInstabilityStatistics.__init__(self, name, FOLLOWER_TEMPORAL_DATA_KEY, "follower", resultsFolderStructure, resultsDir)
        
class SequenceInstabilityStatisticsFriends(SequenceInstabilityStatistics):
    def __init__(self, name, resultsFolderStructure, resultsDir):
        SequenceInstabilityStatistics.__init__(self, name, FRIEND_TEMPORAL_DATA_KEY, "friend", resultsFolderStructure, resultsDir)        
                
class SequenceInstabilityStatisticsAggr(SequenceInstabilityStatistics):
    def __init__(self, name, resultsFolderStructure, resultsDir):
        SequenceInstabilityStatistics.__init__(self, name, AGGR_TEMPORAL_DATA_KEY, "aggr", resultsFolderStructure, resultsDir)        