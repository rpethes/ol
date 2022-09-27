from mpmath import nan

class TemporalData:
    def __init__(self, schoolClass, calculator):
        self._schoolClass = schoolClass
        self._calculator = calculator
        self._errorMessage = ""
    
    def name(self):
        return self._calculator.name()
    
    def calculator(self):
        return self._calculator
    
    
    def __str__(self):
        return self.name()
    
    def writeToFile(self, resultFolder):
        fileName = resultFolder + "/" + self.calculator().fullName() + ".txt"
        f = open(fileName, "w")
        f.write(str(self))
        f.close()
        
    def error(self):
        return self._errorMessage
    
    def setErrorMessage(self, msg):
        self._errorMessage = msg
        

class TemporalDataCalculator:
    def  __init__(self, name, metric_name):
        self._name = name
        self._metric_name = metric_name
        self._full_name = name + "_" + metric_name
        
    def name(self):
        return self._name
    
    def metricName(self):
        return self._metric_name
    
    def fullName(self):
        return self._full_name
    
    def commonStudentsInTurns(self, opinionLeaderMetricList):
        result = []
        n = len(opinionLeaderMetricList)
        if n < 1:
            return result
        
        result = opinionLeaderMetricList[0].network().labels()
        if n > 1:
            commonStudents = set(result)
            rng = range(1,n)
            for i in rng:
                opinionLeaderMetric = opinionLeaderMetricList[i]
                students = set(opinionLeaderMetric.network().labels())
                commonStudents = commonStudents & students
            result = list(commonStudents)
        
        return result
    
    def commonStudentsInConsecutiveTurns(self, opinionLeaderMetricList, turnIndex):
        result = []
        n = len(opinionLeaderMetricList)
        if n <= turnIndex + 1:
            return result
        
        studentset1 = set(opinionLeaderMetricList[turnIndex].idsList())
        studentset2 = set(opinionLeaderMetricList[turnIndex+1].idsList())
        commonStudents = studentset1 & studentset2
        result = list(commonStudents)
        return result
    
    def maximum_minimum_avg_NumberOfStudents(self, opinionLeaderMetricList):
        max_nr = 0
        min_nr = 1000000
        avg_nr = 0.0
        n = len(opinionLeaderMetricList)
        if n < 1:
            return [ nan, nan, nan ]
        rng = range(0,n)
        for i in rng:
            opinionLeaderMetric = opinionLeaderMetricList[i]
            students = set(opinionLeaderMetric.idsList())
            nStudents = len(students)
            max_nr = max(nStudents, max_nr)
            min_nr = min(nStudents, min_nr)
            avg_nr = avg_nr + nStudents
        avg_nr = avg_nr / n
        return [max_nr, min_nr, avg_nr]
        
    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        pass 
        
    
    def createSummaryPlot(self, summaryFile):
        pass
