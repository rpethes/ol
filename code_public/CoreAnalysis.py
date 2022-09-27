from DataReader import DataReader
import numpy as np

class CoreAnalysis(DataReader):
    class Stat:
        def __init__(self):
            self._common_items = None
            self._nr_of_common_items = None
            self._relative_nr_of_common_items = None
            self._opinionLeaderRankCounterMap = dict()
            
        
    def __init__(self,metric_name, metrics, resultsFolderStructure, resultsDir):
        self._metric_name = metric_name
        self._metrics = metrics
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._coreSizeListOfTurns = []
        self._relativeCoreSizeListOfTurns = []
        self._corenessLayersOfTurns = []
        rng = range(5)
        for i in rng:
            self._coreSizeListOfTurns.append(list())
            self._corenessLayersOfTurns.append(list())
            self._relativeCoreSizeListOfTurns.append(list())
        self._turnNrStatMap = dict()
        self._opinionLeaderInCoreCounter = dict()
            
        
    def getDataFrom(self, src, key):
        userData = src.get(self._target_user_data_key)
        if userData == None:
            return None
        data = userData.get(key)
        return data
    
    def areOpinionLeadersInCore(self, coreMetricData, turn):
        for metric in self._metrics:
            name = metric.unique_name()
            opinionLeaderMetricData = self.getOpinionLeaderMetric(turn, name)
            core_set = set(coreMetricData.opinionLeadersList())
            if opinionLeaderMetricData != None:
                metric_opinion_leaders = opinionLeaderMetricData.opinionLeadersList()
                cnt = 0
                for ol in metric_opinion_leaders:
                    if ol in core_set:
                        cnt = cnt + 1 
                pair = self._opinionLeaderInCoreCounter.get(name, None)
                if pair == None:
                    pair = [0,0]
                self._opinionLeaderInCoreCounter[name] = pair
                pair[0] = pair[0] + cnt
                pair[1] = pair[1] + len(metric_opinion_leaders)
            
            
    def processData(self, turnsList, opinionLeaderMetricDataList):
        n = len(turnsList)
        rng = range(n)
        for i in rng:
            turn = turnsList[i]
            coreMetricData = opinionLeaderMetricDataList[i]
            turnIndex = turn.index()
            coreSize = len(coreMetricData._opinionLeaders)
            classSize = len(coreMetricData.network().labels())
            relativeCoreSize = float(coreSize) / float(classSize)
            layers = len(coreMetricData.idsListOfSortedValues())
            self._coreSizeListOfTurns[turnIndex - 1].append(coreSize)
            self._corenessLayersOfTurns[turnIndex - 1].append(layers)
            self._relativeCoreSizeListOfTurns[turnIndex - 1].append(relativeCoreSize)
            self.areOpinionLeadersInCore(coreMetricData, turn)
            
        self.computeStats(opinionLeaderMetricDataList, turnsList)
    
    def computeStats(self, opinionLeaderMetricDataList, turnsList):
        n = len(opinionLeaderMetricDataList)
        statsList = self._turnNrStatMap.get(n, None)
        if statsList == None:
            statsList = []
            self._turnNrStatMap[n] = statsList
        
        stat = self.Stat()
        common_items = None
        for opinionLeaderMetricData in opinionLeaderMetricDataList:
            opinionLeaders = set(opinionLeaderMetricData.opinionLeadersList())
            if common_items == None:
                common_items = opinionLeaders
            else:
                common_items = common_items.intersection(opinionLeaders)
                
        stat._common_items = common_items
        if common_items == None:
            print("wtf")
        stat._nr_of_common_items = len(common_items)
        mean_relRate = 0.0
        for opinionLeaderMetricData in opinionLeaderMetricDataList:
            classSize = len(opinionLeaderMetricData.network().labels())
            relRate = float(stat._nr_of_common_items) / float(classSize)
            mean_relRate += relRate
        mean_relRate = mean_relRate / n
        stat._relative_nr_of_common_items = mean_relRate
        statsList.append(stat)
        
        for metric in self._metrics:
            name = metric.unique_name()
            rank_array = stat._opinionLeaderRankCounterMap.get(name, None)
            if rank_array == None:
                rank_array = []
                for i in range(5):
                    rank_array.append([])
                stat._opinionLeaderRankCounterMap[name] = rank_array
            
            for turn in turnsList:
                turn_index = turn.index()
                opinionLeaderMetricData = self.getOpinionLeaderMetric(turn, name)
                if opinionLeaderMetricData != None:
                    for item in common_items:
                        rank = opinionLeaderMetricData.getRankOfID(item)
                        rank_array[turn_index-1].append(rank)
        
    def getOpinionLeaderMetric(self, turn, metric_name):
        metric_data = turn.get(metric_name)
        return metric_data
    
    def readSchoolClass(self, schoolClass):
        turns = schoolClass.turns()
        turnsList = list()
        opinionLeaderMetricDataList = list()
        for turn in turns:
            opinionLeaderMetric = self.getOpinionLeaderMetric(turn, self._metric_name)
            if opinionLeaderMetric != None:
                turnsList.append(turn)
                opinionLeaderMetricDataList.append(opinionLeaderMetric)
        if len(turnsList) < 1:
            return
        self.processData(turnsList, opinionLeaderMetricDataList)
                
    
          
    def buildStatistics(self, schools):
        stats_file = self._resultsDir + self._metric_name + "_core_analysis_stats.txt";
        f = open(stats_file, "w")
        f.write("Core size of turnes: \n")
        for coreSizeList in self._coreSizeListOfTurns:
            mean = np.mean(coreSizeList)
            var = np.var(coreSizeList)
            f.write(str(mean) + "(" + str(var) + ") ")
        f.write("\n")
        f.write("Relative core size of turnes: \n")
        for coreSizeList in self._relativeCoreSizeListOfTurns:
            mean = np.mean(coreSizeList)
            var = np.var(coreSizeList)
            f.write(str(mean) + "(" + str(var) + ") ")
        f.write("\n")
        f.write("Nr of layers core size of turnes: \n")
        for layerSizeList in self._corenessLayersOfTurns:
            mean = np.mean(layerSizeList)
            var = np.var(layerSizeList)
            f.write(str(mean) + "(" + str(var) + ") ")
        f.write("\n")
        for turnNr, stats in self._turnNrStatMap.items():
            f.write("Statistics for classes with data in " + str(turnNr) + " waves: \n")
            common_item_numbers = []
            rel_common_item_numbers = []
            opinionLeaderRankCounterMap = dict()
            for stat in stats:
                common_item_numbers.append(stat._nr_of_common_items)
                rel_common_item_numbers.append(stat._relative_nr_of_common_items)
                for metric_name, stat_rank_lists in stat._opinionLeaderRankCounterMap.items():
                    rank_lists = opinionLeaderRankCounterMap.get(metric_name, None)
                    if rank_lists == None:
                        rank_lists = [list(), list(), list(), list(), list()]
                        opinionLeaderRankCounterMap[metric_name] = rank_lists
                    for i in range(5):
                        rank_lists[i].extend(stat_rank_lists[i])
            mean_common_items = np.mean(common_item_numbers)
            mean_rel_common_items = np.mean(rel_common_item_numbers)
            var_common_items = np.var(common_item_numbers)
            var_rel_common_items = np.var(rel_common_item_numbers)
            f.write("Mean number of common items: " + str(mean_common_items) + "\n")
            f.write("Variance of common items: " + str(var_common_items) + "\n")
            f.write("Mean number of rel common items: " + str(mean_rel_common_items) + "\n")
            f.write("Variance of rel common items: " + str(var_rel_common_items) + "\n")
            
        
        f.write("Centrality measures in core: \n")
        for measure_name, cnt_pair in self._opinionLeaderInCoreCounter.items():
            rate = float(cnt_pair[0]) / float(cnt_pair[1])
            f.write( measure_name + ": " + str(cnt_pair[0]) + " / " + str(cnt_pair[1]) + " = " + str(rate) + "\n") 
        f.close()
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self.buildStatistics(schools)