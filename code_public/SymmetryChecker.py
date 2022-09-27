from DataReader import DataReader
import FollowerData
import FriendsData
import numpy as np
import matplotlib.pyplot as plt


class SymmetryChecker(DataReader):
    
    def __init__(self, target_user_data_key, prefix, resultsFolderStructure, resultsDir):
        self._resultsFolderStructure = resultsFolderStructure
        self._prefix = prefix
        self._target_user_data_key = target_user_data_key
        self._resultsDir = resultsDir
        self._values = []
        
    def readTurn(self, turn):
        data = turn.get(self._target_user_data_key)
        if data != None:
            symmetry_rate = data._network.computeSymmetryRate()
            self._values.append(symmetry_rate)
            
                
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        
        mean = np.mean(self._values)
        var = np.var(self._values)
        min_value = np.min(self._values)
        max_value = np.max(self._values)
        median = np.median(self._values)
        hist, bins = np.histogram(self._values, bins = 10, range = (min_value, max_value), density = False)
        base_path = self._resultsDir + self._prefix + "_symm"
        targetFilePath = base_path  + "_histogram.png"
        plt.hist(self._values, bins = bins) 
        plt.savefig(targetFilePath)
        plt.close()
        stat_file = base_path + "_stats.txt"
        f = open(stat_file, "w")
        f.write("mean = " + str(mean) + "\n")
        f.write("median = " + str(median) + "\n")
        f.write("variance = " + str(var) + "\n")
        f.write("min = " + str(min_value) + "\n")
        f.write("max = " + str(max_value) + "\n")
        f.write("bins = " + str(bins) + "\n")
        f.write("hist = " + str(hist) + "\n")
        
class FollowerSymmetryChecker(SymmetryChecker):
    def __init__(self, resultsFolderStructure, resultsDir):
        SymmetryChecker.__init__(self, FollowerData.FOLLOWER_DATA_KEY, "follower", resultsFolderStructure, resultsDir)
        
class FriendSymmetryChecker(SymmetryChecker):
    def __init__(self, resultsFolderStructure, resultsDir):
        SymmetryChecker.__init__(self, FriendsData.FRIENDS_DATA_KEY, "friends", resultsFolderStructure, resultsDir)