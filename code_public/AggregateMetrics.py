from DataReader import DataReader
import numpy as np

class AggregateMetrics(DataReader):
    def __init__(self, resultsFolderStructure, resultsDir):
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._metrics = []
        self._metric_files = dict()
        self._opinion_leader_files = dict()
        self._opinion_leader_file_names = dict()
        self._metricMonotonicityValues = dict()
        self._metricOpinionLeaderNumbers = dict()
    
    
    def getMetricOpinionLeaderNumberList(self, metric):
        metric_key = metric.unique_name()
        values = self._metricOpinionLeaderNumbers.get(metric_key)
        if values == None:
            values = []
            self._metricOpinionLeaderNumbers[metric_key] = values
        return values
    
    def getMetricMonotonicityValueList(self, metric):
        metric_key = metric.unique_name()
        values = self._metricMonotonicityValues.get(metric_key)
        if values == None:
            values = []
            self._metricMonotonicityValues[metric_key] = values
        return values
    
    def registerMetric(self, metric):
        self._metrics.append(metric)
        metricFileName = self._resultsDir + "/" + "aggr" + "_" + metric.name() + ".txt"
        f = open(metricFileName, "w")
        self._metric_files[metric.name()] = f
        opinionLeaderFileName = self._resultsDir + "/" + "aggr" + "_" + metric.name() + "_ol.txt"
        f = open(opinionLeaderFileName, "w")
        self._opinion_leader_files[metric.name()] = f
        self._opinion_leader_file_names[metric.name()] = opinionLeaderFileName
        
    def computeMonotonicyStatistics(self, metric, monotonicy_statistics_file):
        metric_key = metric.unique_name()
        monotonicy_values = self.getMetricMonotonicityValueList(metric)
        meanValue = np.mean(monotonicy_values)
        varianceValue = np.var(monotonicy_values)
        medianValue = np.median(monotonicy_values)
        s = metric_key + " : mean = " + str(meanValue) + " variance = " + str(varianceValue) + " median = " + str(medianValue) + "\n"
        monotonicy_statistics_file.write(s)
    
    
    def computeOpinionLeaderNumbersStatistics(self, metric, opinion_leader_statistics_file):
        metric_key = metric.unique_name()
        values = self.getMetricOpinionLeaderNumberList(metric)
        meanValue = np.mean(values)
        varianceValue = np.var(values)
        medianValue = np.median(values)
        n = len(values)
        nr_unique_opinion_leaders = values.count(1)
        s = metric_key + " : mean = " + str(meanValue) + " variance = " + str(varianceValue) + " median = " + str(medianValue) + " unique = " + str(nr_unique_opinion_leaders) + "/" + str(n) + "\n"
        opinion_leader_statistics_file.write(s)
    
    def readTurn(self, turn):
        schoolClass = turn.parent()        
        resultFolder = self._resultsFolderStructure.turnFolderPath(turn)
        for metric in self._metrics:
            result = metric.compute(turn)
            if result == None:
                continue
            key = metric.unique_name()
            turn.add(key, result)
            result.writeToFile(resultFolder, "aggr")
            f = self._metric_files[metric.name()]
            f.write(str(schoolClass.id()) + ";")
            f.write(str(turn.index()) + ";")
            f.write(str(result) + "\n")
            f = self._opinion_leader_files[metric.name()]
            opinion_leaders = result.opinionLeadersList()
            f.write(str(schoolClass.id()) + ";")
            f.write(str(turn.index()) + ";")
            first = True
            for item in opinion_leaders:
                if first == False:
                    f.write(", ")
                else:
                    first = False
                f.write(str(item))
            f.write("\n")
            monotonicity_values = self.getMetricMonotonicityValueList(metric)
            monotonicity_values.append(result.monotonicy())
            
            firstRankSetSizes = self.getMetricOpinionLeaderNumberList(metric)
            nr_opinion_leaders = len(result.opinionLeadersList())
            firstRankSetSizes.append(nr_opinion_leaders)
                
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        
        monotonicy_stat_file_path = self._resultsFolderStructure.rootDir() + "aggr_monotonicy.txt"
        monotonicy_stat_file = open(monotonicy_stat_file_path, "w")
        
        opinion_leader_number_stat_file_path = self._resultsFolderStructure.rootDir() + "aggr_ol_nr_stat.txt";
        opinion_leader_number_stat_file = open(opinion_leader_number_stat_file_path, "w")
        for metric in self._metrics:
            f = self._opinion_leader_files[metric.name()]
            f.flush()
            f.close()
            opinionLeaderFileName = self._opinion_leader_file_names[metric.name()]
            metric.buildSummaryPlot(opinionLeaderFileName)
            metric.buildStatistics(self._resultsDir)
            self.computeMonotonicyStatistics(metric, monotonicy_stat_file)
            self.computeOpinionLeaderNumbersStatistics(metric, opinion_leader_number_stat_file)