from TemporalData import TemporalData, TemporalDataCalculator

class CounterStatistics(TemporalData):
    def __init__(self, schoolClass, calculator):
        TemporalData.__init__(self, schoolClass, calculator)
        self._opinionLeaderCounterDict = dict()
        
    def add(self, studentID):
        cnt = self._opinionLeaderCounterDict.get(studentID)
        if cnt == None:
            cnt = 1
        else:
            cnt = cnt + 1
        self._opinionLeaderCounterDict[studentID] = cnt
        
    def __str__(self):
        keys = self._opinionLeaderCounterDict.keys()
        s = str()
        for key in keys:
            value = self._opinionLeaderCounterDict.get(key)
            s += key + ";" + str(value) + "\n"
        return s
        
        

class CounterStatisticsCalculator(TemporalDataCalculator):
    def __init__(self, metric_name):
        TemporalDataCalculator.__init__(self, "counter_statistics", metric_name)
        
    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        result = CounterStatistics(schoolClass, self)
        for metric in opinionLeaderMetricList:
            olList = metric.opinionLeadersList()
            for ol in olList:
                result.add(ol)
                
        return result
        
    def createSummaryPlot(self, summaryFile):
        pass