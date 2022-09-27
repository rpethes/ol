from TemporalStatBuilder import TemporalStatBuilder
from TemporalDataBuilder import FOLLOWER_TEMPORAL_DATA_KEY
from TemporalDataBuilder import FRIEND_TEMPORAL_DATA_KEY
import numpy as np
import matplotlib.pyplot as plt


def distanceFromMean(x, mean):
    return abs(x - mean)

class JaccardSimilarityStatistics(TemporalStatBuilder):
    def __init__(self, name, target_user_data_key, prefix, resultsFolderStructure, resultsDir):
        TemporalStatBuilder.__init__(self, name, target_user_data_key, prefix, resultsFolderStructure, resultsDir)
        self._values = []
        self._turnLevelValues = {}
        self._valueDict = {}
        
    
    def processData(self, data, schoolClass):
        self._values.extend(data._values)
        turnObjects = schoolClass.turns()
        turns = []
        for turn in turnObjects:
            turns.append(turn.index())
        n = len(data._values)
        rng = range(n)
        for i in rng:
            value = data._values[i]
            fromTurn = turns[i]
            toTurn = turns[i + 1]
            key = (fromTurn, toTurn)
            valueList = None
            if key in self._turnLevelValues.keys():
                valueList = self._turnLevelValues[key]
            else:
                valueList = []
                self._turnLevelValues[key] = valueList 
            valueList.append(value)
            
            itemsWithTheSameValue = None
            if value in self._valueDict:
                itemsWithTheSameValue = self._valueDict[value]
            else:
                itemsWithTheSameValue  = []
                self._valueDict[value] = itemsWithTheSameValue 
            itemsWithTheSameValue.append([schoolClass, key])
    
    def buildStatistics(self, schools):
        mean = np.mean(self._values)
        var = np.var(self._values)
        min_value = np.min(self._values)
        max_value = np.max(self._values)
        hist, bins = np.histogram(self._values, bins = 10, range = (min_value, max_value), density = False)
        base_path = self._resultsDir + self._prefix + self._name
        targetFilePath = base_path  + "_histogram.png"
        plt.hist(self._values, bins = bins) 
        plt.xlabel("Jaccard similarity", fontweight='normal', fontsize=14)
        plt.ylabel("Frequency", fontweight='normal', fontsize=14)
        plt.savefig(targetFilePath)
        plt.close()
        stat_file = base_path + "_stats.txt"
        f = open(stat_file, "w")
        f.write("mean = " + str(mean) + "\n")
        f.write("variance = " + str(var) + "\n")
        f.write("min = " + str(min_value) + "\n")
        f.write("max = " + str(max_value) + "\n")
        f.write("bins = " + str(bins) + "\n")
        f.write("hist = " + str(hist) + "\n")
        
        keys = self._turnLevelValues.keys()
        for key in keys:
            values = self._turnLevelValues[key] 
            m = np.mean(values)
            var = np.var(values)
            min_value = np.min(values)
            max_value = np.max(values)
            hist, bins = np.histogram(values, bins = 10, range = (min_value, max_value), density = False)
            f.write(str(key) + " mean = " + str(m) + " variance = " + str(var) + " min = " + str(min_value) + " max = " + str(max_value) +"\n")
        
        values = list(self._valueDict.keys())
        values.sort(key = (lambda x : abs(x - mean)))
        n = min(10, len(values))
        for i in range(n):
            v = values[i]
            f.write("distance = " + str(abs(v - mean)))
            l = self._valueDict[v]
            for data in l:
                index = data[1]
                schoolClass = data[0]
                id = schoolClass.id() 
                f.write(" schoolClass: " + str(id) + " index = " + str(index))
            f.write("\n")
        f.close()
        
class JaccardSimilarityStatisticsFollowerData(JaccardSimilarityStatistics):
    def __init__(self, name, resultsFolderStructure, resultsDir):
        JaccardSimilarityStatistics.__init__(self, name, FOLLOWER_TEMPORAL_DATA_KEY, "follower", resultsFolderStructure, resultsDir)
        
class JaccardSimilarityStatisticsFrieendsData(JaccardSimilarityStatistics):
    def __init__(self, name, resultsFolderStructure, resultsDir):
        JaccardSimilarityStatistics.__init__(self, name, FRIEND_TEMPORAL_DATA_KEY, "friend", resultsFolderStructure, resultsDir)