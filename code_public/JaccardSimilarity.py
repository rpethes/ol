from TemporalData import TemporalData, TemporalDataCalculator

class JaccardSimilarity(TemporalData):
    def __init__(self, schoolClass, calculator):
        TemporalData.__init__(self, schoolClass, calculator)
        self._values = []
    
    def add(self, value):
        self._values.append(value)
    
    
    def __str__(self):
        s = str(self._schoolClass.id())
        if (self._errorMessage != None) and len(self._errorMessage) > 0:
            s = s + ";" + self._errorMessage + "\n"
            return s
            
        for value in self._values:
            s = s + ";" + str(value)
        s = s + "\n"
        return s
        
class JaccardSimilarityCalculator(TemporalDataCalculator):
    def __init__(self, metric_name, type):
        TemporalDataCalculator.__init__(self, "jaccard_" + type, metric_name)
        self._type = type
        
    
    def neighbours(self, network):
        return network.neighbors(self._type)
    
    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        result = JaccardSimilarity(schoolClass, self)
        students = self.commonStudentsInTurns(opinionLeaderMetricList)
        nr_of_students = len(students)
        if nr_of_students < 1:
            result.setErrorMessage("number of common students is zero")
            return result
              
        n = len(opinionLeaderMetricList)
        if n < 1:
            return result
        
        neighbours1 = self.neighbours(opinionLeaderMetricList[0].network())
        rng = range(1, n)
        for i in rng:
            neighbours2 = self.neighbours(opinionLeaderMetricList[i].network())
            jaccard_sim = 0.0
            for student_id in students:
                s1 = set(neighbours1[student_id])
                s2 = set(neighbours2[student_id])
                nunion = len(s1 | s2)
                jaccard_of_node = 1.0
                if nunion > 0:
                    nintersection = len(s1 & s2)
                    jaccard_of_node = float(nintersection)/float(nunion)
                jaccard_sim = jaccard_sim + jaccard_of_node
            jaccard_sim = jaccard_sim / nr_of_students
            result.add(jaccard_sim)
            neighbours1 = neighbours2

        return result
    