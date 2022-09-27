from TemporalData import TemporalData, TemporalDataCalculator
import itertools

class SequenceInstability(TemporalData):
    def __init__(self, schoolClass, calculator):
        TemporalData.__init__(self, schoolClass, calculator)        
        self._value = None
        self._sequenceLen = None
    
    
    
    def __str__(self):
        s = str(self._schoolClass.id())
        if (self._errorMessage != None) and len(self._errorMessage) > 0:
            s = s + ";" + self._errorMessage + "\n"
            return s
            
        s = s + ";" + str(self._value) + "\n"
        return s
    
    def setValue(self, v):
        self._value = v
        
    def getValue(self):
        return self._value
    
    def setSequenceLen(self, sequenceLen):
        self._sequenceLen = sequenceLen;
        
    def getSequenceLen(self):
        return self._sequenceLen
    
    
class SequenceInstabilityCalculator(TemporalDataCalculator):
    def __init__(self, metric_name):
        TemporalDataCalculator.__init__(self, "sequence_instability", metric_name)
    
    def computeDescartesProduct(self, opinionLeaderMetricList):
        opinion_leader_lists = []
        for metric in opinionLeaderMetricList:
            opinion_leader_lists.append(metric.opinionLeadersList())
        product = itertools.product(*opinion_leader_lists)
        ret = []
        for item in product:
            ret.append(item)
        return ret
    
    def computeInstabilityOfSequence(self, seq):
        n = len(seq)
        items = set()
        prev = seq[0]
        items.add(prev)
        inc = 1.0 / n
        rng = range(1,n)
        ret = 0.0
        for i in rng:
            current_item = seq[i]
            if current_item != prev:
                if current_item in items:
                    ret = ret + inc 
                else:
                    ret = ret + 1.0
                    items.add(current_item)
            prev = current_item
        return ret/(n-1)
    
        
    
    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        result = SequenceInstability(schoolClass, self)
        opinion_leader_lists = self.computeDescartesProduct(opinionLeaderMetricList)
        d = 0.0
        for opinion_leader_list in opinion_leader_lists:
            d = d + self.computeInstabilityOfSequence(opinion_leader_list)
        n = len(opinion_leader_lists)
        result.setValue(d / n)    
        return result


class SequenceInstabilityWithJaccardCalculator(TemporalDataCalculator):
    def __init__(self, metric_name):
        TemporalDataCalculator.__init__(self, "sequence_instability", metric_name)
    
    
    def jaccard(self, s1, s2):
        uni = frozenset.union(s1, s2)
        if len(uni) < 1:
            return 1.0
        ints = frozenset.intersection(s1, s2)
        ret = float(len(ints)) / float(len(uni))
        return ret
    
    def computeInstabilityOfSequence(self, opinion_leader_sets_lists):
        n = len(opinion_leader_sets_lists)
        items = set()
        prev = opinion_leader_sets_lists[0]
        items.add(prev)
        inc = 1.0 / n
        rng = range(1,n)
        ret = 0.0
        for i in rng:
            current_item = opinion_leader_sets_lists[i]
            if current_item != prev:
                if current_item in items:
                    ret = ret + inc 
                else:
                    m = 0.0
                    for item in items:
                        jacc = self.jaccard(current_item, item)
                        if jacc > m:
                            m = jacc
                    ret = ret + 1.0 - m
                    items.add(current_item)
            prev = current_item
        return ret/(n-1)
    
        
    
    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        result = SequenceInstability(schoolClass, self)
        opinion_leader_sets_lists = []
        for metric in opinionLeaderMetricList:
            opinion_leader_sets_lists.append(frozenset(metric.opinionLeadersList()))
        d = self.computeInstabilityOfSequence(opinion_leader_sets_lists)
        result.setValue(d)
        result.setSequenceLen(len(opinionLeaderMetricList))
        return result
        
    