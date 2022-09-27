import numpy as np
import scipy.stats

class OpinionLeaderMetricData:
    
    def __init__(self, name, uniqueName):
        self._name = name
        self._uniqueName = uniqueName
        self._values = {}
        self._ids = []
        self._value_id_dict = {}
        self._sorted_value_list = []
        self._ids_of_sorted_value_list = []
        self._opinionLeaders = None
        self._network = None
        self._ecdf = None
        self._monotonicy = None
    
    def name(self):
        return self._name
    
    def unique_name(self):
        return self._uniqueName
    
    def idToValueDict(self):
        return self._values
    
    def idsList(self):
        return self._ids
    
    def valueToIDDict(self):
        return self._value_id_dict
    
    def sortedValueList(self):
        return self._sorted_value_list
    
    def idsListOfSortedValues(self):
        return self._ids_of_sorted_value_list
    
    def opinionLeadersList(self):
        return self._opinionLeaders
    
    def network(self):
        return self._network
    
    def __str__(self):
        s = str(self.sortedValueList()) + ";"
        s = s + str(self.idsListOfSortedValues())
        return s
    
    def writeToFile(self, resultFolder, prefix):
        fileName = resultFolder + "/" + prefix + "_" + self.name() + ".txt"
        f = open(fileName, "w")
        f.write(str(self))
        f.close()

    def getRankOfID(self, ID):
        rank = None
        n = len(self._ids_of_sorted_value_list)
        rng = range(n)
        for i in rng:
            l = self._ids_of_sorted_value_list[i]
            if ID in l:
                rank = i + 1
                break
        return rank
    
    def ecdf(self):
        return self._ecdf
    
    def monotonicy(self):
        return self._monotonicy
    
class OpinionLeaderMetric:
    def __init__(self, name, networkID):
        self._name = name
        self._networkID = networkID
        self._uniqueName = networkID + "_" + name
        
               
    def name(self):
        return self._name
    
    def unique_name(self):
        return self._uniqueName
     
    def networkID(self):
        return self._networkID
    
    def compute_values(self, network):
        empty_dict = dict()
        return empty_dict
    
    def compute(self, network):
        result = OpinionLeaderMetricData(self.name(), self.unique_name()) 
        result._values = self.compute_values(network)
        if result._values == None:
            return None
        result._ids = result._values.keys()
        result._value_id_dict = dict()
        result._network = network
        
        for id in result._ids:
            value = result._values[id]
            value_list = result._value_id_dict.get(value)
            if value_list == None:
                value_list = []
            value_list.append(id)
            result._value_id_dict[value] = value_list
        
        
        result._sorted_value_list = list(result._value_id_dict.keys())
        result._sorted_value_list.sort(reverse=True)
        result._ids_of_sorted_value_list = []
        for v in result._sorted_value_list:
            result._ids_of_sorted_value_list.append(result._value_id_dict[v])
        
        result._opinionLeaders = None
        if result._ids_of_sorted_value_list != None and len(result._ids_of_sorted_value_list) > 0:
            result._opinionLeaders = result._ids_of_sorted_value_list[0]
        print(result._opinionLeaders)
        
        node_nr = len(result._ids)
        
        #compute monotonicity
        s = 0.0
        rank_nr = 0
        for ids_with_same_rank in result._value_id_dict.values():
            nItemWithSameRank = len(ids_with_same_rank)
            s += nItemWithSameRank*(nItemWithSameRank - 1)
            rank_nr += 1 
        
        s = float(s) / (node_nr * (node_nr - 1))
        m = (1.0 - s) * (1.0 - s)
        result._monotonicy = m  
        return result   
            
    def buildSummaryPlot(self, summaryFile):
        class_counter = dict()
        with open(summaryFile) as fp:
            line = fp.readline()
            while line:
                tokens = line.split(";", 3)
                if len(tokens) == 3:
                    classIDs = tokens[0].strip()
                    cnt = class_counter.get(classIDs, 0)
                    cnt = cnt + 1
                    class_counter[classIDs] = cnt
                line = fp.readline()
        
        counter_map = dict()
        
        with open(summaryFile) as fp:
            line = fp.readline()
            while line:
                tokens = line.split(";", 3)
                if len(tokens) == 3:
                    classIDs = tokens[0].strip()
                    nr_of_terms = class_counter[classIDs]
                    counter = counter_map.get(nr_of_terms, None)
                    if counter == None:
                        counter = dict()
                        counter_map[nr_of_terms] = counter
                    studentIDs = tokens[2].strip()
                    studentIDList = studentIDs.split(", ")
                    for studentID in studentIDList:
                        if studentID in counter:
                            counter[studentID] = counter[studentID] + 1
                        else: 
                            counter[studentID] = 1
                line = fp.readline()
        
        histogramValues = summaryFile[0:len(summaryFile)-4] + "_histogram.txt"
        f = open(histogramValues,"w")
        for turn_nr, counter in counter_map.items():
            values = sorted(counter.values())
            m = values[len(values) - 1]
            hist = m * [0]
            keys = counter.keys()
            for key in keys:
                val = counter[key]
                hist[val - 1] = hist[val - 1] + 1
            xvalues = m * [0]
            xlabels = m * ["0"]
            for i in range(m):
                xvalues[i] = i + 1
                xlabels[i] = str(xvalues[i]) 
            f.write("Waves : " + str(turn_nr))
            f.write("\n")
            f.write(str(xlabels))
            f.write("\n")
            rng = range(len(hist))
            for i in rng:
                f.write(str(hist[i]))
                if i < turn_nr - 1:
                    f.write(" & ")
            f.write("\n")
        f.close()
        
              
class InDegreeMetric(OpinionLeaderMetric):
    
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "InDegree", networkID)
    
    def compute_values(self, network):
        return network.inDegree()


class NeighborhoodInMetric(OpinionLeaderMetric):
    
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "NeighborhoodIn", networkID)
    
    def compute_values(self, network):
        return network.neighborhood(1, "in")

class TwoHopNeighborhoodInMetric(OpinionLeaderMetric):
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "TwoHopNeighborhoodIn", networkID)
    
    def compute_values(self, network):
        return network.neighborhood(2, "in")

class CorenessInMetric(OpinionLeaderMetric):
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "CorenessIn", networkID)
    
    def compute_values(self, network):
        return network.coreness("in")

class PageRank65Metric(OpinionLeaderMetric):
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "PageRank65", networkID)
        self._damping_value = 0.65
    
    def compute_values(self, network):
        return network.pageRank(self._damping_value)
    
class ClosenessMetric(OpinionLeaderMetric):
    
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "Closeness", networkID)
    
    def compute_values(self, network):
        return network.closeness()

class BetweennessMetric(OpinionLeaderMetric):
    
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "Betweenness", networkID)
    
    def compute_values(self, network):
        return network.betweenness(asDirected = False)
        
class DirectedEigenMetric(OpinionLeaderMetric):
    
    def __init__(self, networkID):
        OpinionLeaderMetric.__init__(self, "DirectedEigen", networkID)
    
    def compute_values(self, network):
        return network.eigen_centralty(asDirected = False)
        

class BordaCountAggregationMetric(OpinionLeaderMetric):
    def __init__(self, name, trhL, trhU, metrics):
        OpinionLeaderMetric.__init__(self, name, "aggr")
        self._metrics = metrics
        self._trhU = trhU
        self._trhL = trhL
        self._selectedAggregationsDict = dict()
        self._selectedMeasuresDict = dict()
    
    
    def computeCorrelation(self, rowMetricDataObj, colMetricDataObj, IDSet):   
        row_values = []
        col_values = []
        rowIDtoValue = rowMetricDataObj.idToValueDict()
        colIDtoValue = colMetricDataObj.idToValueDict()
        for student_id in IDSet:
            row_values.append(rowIDtoValue[student_id])
            col_values.append(colIDtoValue[student_id])
        tau, p_value = scipy.stats.kendalltau(row_values, col_values)
        return tau
    
    def computeCorrelationMatrix(self, metricDataList, IDSet):
        mx = []
        n = len(metricDataList)
        rng = range(n)
        for i in rng:
            rowMetricData = metricDataList[i]
            row = []
            for j in rng:
                if j < i:
                    row.append(mx[j][i])
                if j == i:
                    row.append(1.0)
                if j > i:
                    colMetricData = metricDataList[j]
                    correlation_value = self.computeCorrelation(rowMetricData, colMetricData, IDSet)
                    if correlation_value < 0.0:
                        correlation_value = 0.0
                    row.append(correlation_value)
            mx.append(row)
        return mx
    
    def sliceing(self, metricDataList, mxCorrelation):
      
        n = len(metricDataList)
        rng = range(n)
        S = set()
        for i in rng:
            high_corr_of_i = set()
            low_corr_of_i = set()
            high_corr_of_i.add(i)
            low_corr_of_i.add(i)
            rng2 = range( i + 1, n)
            row = mxCorrelation[i]
            for j in rng2:
                val = row[j]
                if np.isnan(val):
                    continue
                if val >= self._trhU:
                    high_corr_of_i.add(j)
                if val <= self._trhL:
                    low_corr_of_i.add(j)
            S.add(frozenset(high_corr_of_i))
            S.add(frozenset(low_corr_of_i))
            S.add(frozenset(set.union(high_corr_of_i, low_corr_of_i))) 
         
        return S          
    
    def selection(self, S, mxCorr):
        subset_entripy_pairs = []
        for s in S:
            N = len(s)
            if N < 2:
                continue
            row_index = min(s)
            row_in_mxCorr = mxCorr[row_index]
            
            sum_corr = 0.0
            for i in s:
                sum_corr+= row_in_mxCorr[i]
            entropy = 0.0
            for i in s:
                m = row_in_mxCorr[i] / sum_corr
                if m > 1e-9:
                    entropy += m * np.log(m)
            entropy *= -1.0/N;
            p = (s, entropy)
            subset_entripy_pairs.append(p)
        subset_entripy_pairs.sort(key= lambda tup: tup[1], reverse=True)
        first = subset_entripy_pairs[0]
        if len(subset_entripy_pairs) < 2:
            return first[0]
        second = subset_entripy_pairs[1]
        selected = frozenset.union(first[0], second[0])
        return selected
    
    def bordaCount(self, selectedMeasures, IDSet, metricDataList):
        scores = dict()
        C = float(len(IDSet))
        for ID in IDSet:
            score_of_item = 0.0
            for measureIndex in selectedMeasures:
                metricData = metricDataList[measureIndex]
                rank = metricData.getRankOfID(ID)
                score_of_item += C - rank
            scores[ID] = score_of_item
        return scores
    
    def aggregate(self, metricDataList, IDSet):
        mxCorr = self.computeCorrelationMatrix(metricDataList, IDSet)
        S = self.sliceing(metricDataList, mxCorr)
        selected = self.selection(S, mxCorr)
        result = self.bordaCount(selected, IDSet, metricDataList)
        selected_names = []
        for idx in selected:
            selected_names.append(metricDataList[idx].unique_name())
        selected_names_set = frozenset(selected_names)
        cnt = self._selectedAggregationsDict.get(selected_names_set, 0)
        cnt += 1
        self._selectedAggregationsDict[selected_names_set] = cnt
        
        for name in selected_names:
            cnt = self._selectedMeasuresDict.get(name, 0)
            cnt += 1
            self._selectedMeasuresDict[name] = cnt
            
        return result
    
    def compute(self, turn):
        result = OpinionLeaderMetricData(self.name(), self.unique_name()) 
        result._values = self.compute_values(turn)
        if result._values == None:
            return None
        result._ids = result._values.keys()
        result._value_id_dict = dict()
        result._network = None
        
        for id in result._ids:
            value = result._values[id]
            value_list = result._value_id_dict.get(value)
            if value_list == None:
                value_list = []
            value_list.append(id)
            result._value_id_dict[value] = value_list
        
        
        result._sorted_value_list = list(result._value_id_dict.keys())
        result._sorted_value_list.sort(reverse=True)
        result._ids_of_sorted_value_list = []
        for v in result._sorted_value_list:
            result._ids_of_sorted_value_list.append(result._value_id_dict[v])
        
        result._opinionLeaders = None
        if result._ids_of_sorted_value_list != None and len(result._ids_of_sorted_value_list) > 0:
            result._opinionLeaders = result._ids_of_sorted_value_list[0]
        print(result._opinionLeaders)
        
        node_nr = len(result._ids)
        #compute monotonicity
        s = 0.0
        rank_nr = 0
        for ids_with_same_rank in result._value_id_dict.values():
            nItemWithSameRank = len(ids_with_same_rank)
            s += nItemWithSameRank*(nItemWithSameRank - 1)
            rank_nr += 1 
        
        s = float(s) / (node_nr * (node_nr - 1))
        m = (1.0 - s) * (1.0 - s)
        result._monotonicy = m  
        return result
    
    def compute_values(self, turn):
        metricDataList = []
        IDSet = None
        for metric in self._metrics:
            metricKey = metric.unique_name()
            if turn.hasKey(metricKey) == False:
                return None
            metricData = turn.get(metricKey)
            metricDataList.append(metricData)
            IDList = metricData.idsList()
            if IDSet == None:
                IDSet = set(IDList)
            else:
                IDSet = IDSet & set(IDList)
        
        result = self.aggregate(metricDataList, IDSet)
        return result

    def buildStatistics(self, resultDir):
        summaryFilePath = resultDir + "/" + self._name + "_aggrStat.txt"
        f = open(summaryFilePath, "w")
        n = 0
        for key, value in self._selectedAggregationsDict.items():
            row = str(key) + " : " + str(value) + "\n"
            n += value
            f.write(row)
        
        for name, cnt in self._selectedMeasuresDict.items():
            row = name + ":" + str(cnt) + " ( " + str(100.0 * float(cnt)/n) + "% )\n"
            f.write(row)
        f.close()