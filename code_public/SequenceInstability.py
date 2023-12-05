from TemporalData import TemporalData, TemporalDataCalculator
import itertools
import numpy as np
from test.test_smtplib import sim_auth
import copy
from ResultsFolderStructure import ResultsFolderStructure

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


Jaccard = "Jaccard_Distance"
AdjJaccard = "Adjusted_Jaccard_Distance"
SFH = "SpearmanFootruleHausdorff"

class SequenceInstabilityTopInfluencers(TemporalDataCalculator):
    def __init__(self, metric_name, k, type):
        TemporalDataCalculator.__init__(self, "sequence_instability_top_" + str(k) +" _" + type if k > 1 else "sequence_instability", metric_name)
        self._k = k
        self._type = type
        if k < 2:
            self._type = Jaccard
        self._beta = 0.9999
        self._maxSpearmanFoolrule = (k + 1)*k
        self._exponential_smoothing_constant = 1.0
        self._sigma_epsilon = 0.0001


    def createRankedListsWithoutTies(self, w):
        filtered_list = []
        for items_of_rank in w:
            if len(items_of_rank) > 0:
                filtered_list.append(items_of_rank)
        res = list(itertools.product(*filtered_list))
        return res

    def spearman_foolrule(self, x, y, item_ranks_x, item_ranks_y):
        s1 = frozenset(x)
        s2 = frozenset(y)
        common_items = frozenset.intersection(s1, s2)
        ret = 0.0
        for item in common_items:
            ret = ret + abs(item_ranks_x[item] - item_ranks_y[item])

        for item in x:
            if item not in common_items:
                ret = ret + self._k - abs(item_ranks_x[item])

        for item in y:
            if item not in common_items:
                ret = ret + self._k - abs(item_ranks_y[item])


        ret = ret / self._maxSpearmanFoolrule
        return ret

    def builldItemRankMap(self, w):
        ret = dict()
        r = range(len(w))
        for rank in r:
            items_of_rank = w[rank]
            for item in items_of_rank:
                ret[item] = rank
        return ret


    def hausdorff_distance(self,w1, w2):
        wl1 = self.createRankedListsWithoutTies(w1)
        wl2 = self.createRankedListsWithoutTies(w2)

        item_ranks1 = self.builldItemRankMap(w1)
        item_ranks2 = self.builldItemRankMap(w2)
        nrows = len(wl1)
        ncols = len(wl2)
        distance_matrix = np.zeros((nrows, ncols))
        row_rng = range(nrows)
        col_rng = range(ncols)
        for row in row_rng:
            for col in col_rng:
                d = self.spearman_foolrule(wl1[row], wl2[col], item_ranks1, item_ranks2)
                distance_matrix[row,col] = d
        row_minimums = distance_matrix.min(axis = 1)
        col_minimums = distance_matrix.min(axis = 0)
        row_maxmin = row_minimums.max()
        col_maxmin = col_minimums.max()
        ret = max(row_maxmin, col_maxmin)
        return ret


    def rank_distance(self, w1, w2):
        return self.hausdorff_distance(w1,w2)

    def adjusted_jaccard_distance(self, w1, w2):
        l1 = []
        l2 = []
        for l in w1:
            l1 = l1 + l
        for l in w2:
            l2 = l2 + l
        s1 = frozenset(l1)
        s2 = frozenset(l2)
        uni = frozenset.union(s1, s2)
        if len(uni) < 1:
            return 1.0
        symmetric_difference = frozenset.symmetric_difference(s1, s2)
        rank_dist = 0.0
        if self._beta > 0.0:
            rank_dist = self.rank_distance(w1, w2)
        ret = (float(len(symmetric_difference)) + self._beta * rank_dist) / (float(len(uni)) + self._beta)
        return ret


    # def computeInstabilityOfTopKSequence(self, list_of_top_k_lists):
    #     n = len(list_of_top_k_lists)
    #     ret = 0.0
    #     r = range(1,n)
    #     p = 1.0 / float(n)
    #     for i in r:
    #         current_top_k_list = list_of_top_k_lists[i]
    #         prev_top_k_list = list_of_top_k_lists[i-1]
    #         D = self.adjusted_jaccard_distance(prev_top_k_list, current_top_k_list)
    #         if D == 0.0:
    #             continue
    #         r2 = range(i-1)
    #         for j in r2:
    #             top_k_list = list_of_top_k_lists[j]
    #             d = self.adjusted_jaccard_distance(top_k_list, current_top_k_list)
    #             if d < D:
    #                 D = d
    #         ret = ret + p + D * (1 - p)
    #     ret = ret / ( n - 1)
    #     return ret
    #

    def jaccard_distance(self, w1, w2):
        l1 = []
        l2 = []
        for l in w1:
            l1 = l1 + l
        for l in w2:
            l2 = l2 + l
        s1 = frozenset(l1)
        s2 = frozenset(l2)
        uni = frozenset.union(s1, s2)
        if len(uni) < 1:
            return 1.0
        symmetric_difference = frozenset.symmetric_difference(s1, s2)
        ret = float(len(symmetric_difference)) / float(len(uni))
        return ret
    
    def similarity_distance(self, w1, w2):
        if self._type == SFH:
            return self.hausdorff_distance(w1,w2)
        
        if self._type == AdjJaccard:
            return self.adjusted_jaccard_distance(w1,w2)
        
        return self.jaccard_distance(w1, w2)
   

    def create_similarity_matrix(self, list_of_top_k_lists):
        mx = []
        n = len(list_of_top_k_lists)
        rows = range(0,n)
        cols = range(0,n)
        for row in rows:
            current_row = []
            row_item = list_of_top_k_lists[row]
            for col in cols:
                if row == col:
                    current_row.append(1.0)
                elif row < col:
                    col_item = list_of_top_k_lists[col]
                    similarity = 1.0 - self.similarity_distance(row_item, col_item)
                    current_row.append(similarity)
                else:
                    similarity = mx[col][row]
                    current_row.append(similarity)
            mx.append(current_row)
        return mx


    def compute_lambda(self, similarity_matrix, target_file_path_prefix):
        mx = copy.deepcopy(similarity_matrix)
        n = len(mx)
        rows = range(0,n)
        lmbd = 0
        covering_threshold = 0.0
        for row in rows:
            cols = range(row,n)
            s = 0.0
            for col in cols:
                sim = mx[row][col]
                s = s + sim
                if col > row and sim > 0.0:
                    line_at_col = mx[col]
                    rng = range(0,n)
                    for i in rng:
                        item = line_at_col[i]
                        covering = item - sim
                        if covering > 0.0:
                            line_at_col[i] = covering
                        else:
                            line_at_col[i] = 0.0
            if s > covering_threshold:
                lmbd = lmbd + min(s,1.0)
            if target_file_path_prefix != None:
                target_file_path = target_file_path_prefix + "_lambda_step_" + str(row + 1) + ".txt"
                self.save_similarity_matrix(mx, target_file_path)
                
        return lmbd

    def compute_neighbourhood_differeces(self, similarity_matrix):
        d = 0.0
        r = range(len(similarity_matrix) - 1)
        for i in r:
            step_distance = 1.0 - similarity_matrix[i][i + 1]
            d = d + step_distance
        return d

    def save_similarity_matrix(self, mx, target_file_path):
        n = len(mx)
        header = " / "
        rng = range(n)
        for i in rng:
            header = header + "& S(" + str(i + 1) + ")"
            
        header = header + " \\\\\n"
        f = open(target_file_path, "w")
        f.write(header)
        
        for i in rng:
            line = "S(" + str(i + 1) + ")"
            rng2 = range(n)
            row = mx[i]
            for j in rng2:
                val = row[j]
                line = line + " & " + str(val)
            line = line + " \\\\\n"
            f.write(line)
        f.close()
        
    def computeInstabilityOfTopKSequence(self, list_of_top_k_lists, target_file_path_prefix):
        n = len(list_of_top_k_lists)
        sigma = 1.0 / (n-1) - self._sigma_epsilon
        normalizer_factor = (n - 1) * (1 + sigma)
        similarity_matrix = self.create_similarity_matrix(list_of_top_k_lists)
        if target_file_path_prefix != None:
            target_file_path = target_file_path_prefix + ".txt" 
            self.save_similarity_matrix(similarity_matrix, target_file_path)
        lmbd = self.compute_lambda(similarity_matrix, target_file_path_prefix)
        step_distances = self.compute_neighbourhood_differeces(similarity_matrix)
        ret = (lmbd + sigma * step_distances - 1.0) / normalizer_factor
        return ret

    def calc(self, schoolClass, turnsList, opinionLeaderMetricList):
        result = SequenceInstability(schoolClass, self)
        list_of_top_k_lists = []
        top_k_range = range(self._k)
        for metric in opinionLeaderMetricList:
            ordered_list = metric.idsListOfSortedValues()
            top_k_list = []
            for i in top_k_range:
                if i < len(ordered_list):
                    top_k_list.append(ordered_list[i])
                else:
                    top_k_list.append([])
            list_of_top_k_lists.append(top_k_list)
        d = self.computeInstabilityOfTopKSequence(list_of_top_k_lists, None)
        result.setValue(d)
        result.setSequenceLen(len(opinionLeaderMetricList))
        return result


test_list = []
test_list_item1 = [['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J']]
test_list_item2 = [['J'], ['I'], ['H'], ['G'], ['F'], ['E'], ['D'], ['C'], ['B'], ['A']]
test_list_item3 = [['F'], ['G'], ['H'], ['I'], ['J'], ['A'], ['B'], ['C'], ['D'], ['E']]
test_list_item4 = [['E'], ['D'], ['C'], ['B'], ['A'], ['J'], ['I'], ['H'], ['G'], ['F']]
test_list_item5 = [['G'], ['A'], ['E'], ['B'], ['C'], ['I'], ['D'], ['F'], ['H'], ['J']]

test_list.append(test_list_item1)
test_list.append(test_list_item2)
test_list.append(test_list_item3)
test_list.append(test_list_item4)
test_list.append(test_list_item5)

class SequenceInstabilityTopInfluencers_SFH(SequenceInstabilityTopInfluencers):
    def __init__(self, metric_name, k):
        SequenceInstabilityTopInfluencers.__init__(self, metric_name, k, SFH)

    def similarity_distance(self, w1, w2):
        return self.hausdorff_distance(w1,w2)

class SequenceInstabilityTopInfluencersTester:

    def __init__(self, resultsFolderStructure, test_lists):
        self._resultsFolderStructure = resultsFolderStructure
        self._test_lists = test_lists
    
    
    def saveTable(self, instability_values_jaccard_distance, instability_values_adjusted_jaccard_distance, instability_values_SFH_distance, targetFilePath):
        header = "k & d_J & d_beta & d_SFH \\\\\n"
        f = open(targetFilePath, "w")
        f.write(header)
        n = len(instability_values_jaccard_distance)
        rng = range(n)
        for k in rng:
            line = str(k + 1) + " & " + str(instability_values_jaccard_distance[k]) + " & " + str(instability_values_adjusted_jaccard_distance[k]) + " & " + str(instability_values_SFH_distance[k])
            line = line + " \\\\\n" 
            f.write(line)
        f.close()
        
    def run(self):
        max_sequence_length = 0
        for item in self._test_lists:
            len_list = len(item)
            if len_list > max_sequence_length:
                max_sequence_length = len_list

        range_k = range(max_sequence_length)
        range_sequence = range(len(self._test_lists))
        list_of_top_k_lists = []
        instability_values_jaccard_distance = []
        instability_values_adjusted_jaccard_distance = []
        instability_values_SFH_distance = []
        
        testDir = self._resultsFolderStructure.instabilityTestDir()
        for _ in self._test_lists:
            list_of_top_k_lists.append([])
        for k in range_k:
            for i in range_sequence:
                list_ith = self._test_lists[i]
                if len(list_ith) > k:
                    list_of_top_k_lists[i].append(list_ith[k])
            
            pathPrefixJaccard = testDir + self._resultsFolderStructure.pathSep() + "Jaccard_k" + str(k+1)
            calculator_Jaccard_distance = SequenceInstabilityTopInfluencers("test", k + 1, Jaccard)
            instability_jaccard = calculator_Jaccard_distance.computeInstabilityOfTopKSequence(list_of_top_k_lists, pathPrefixJaccard)
            instability_values_jaccard_distance.append(instability_jaccard)

            pathPrefixAdjJaccard = testDir + self._resultsFolderStructure.pathSep() + "adj_Jaccard_k" + str(k+1)
            calculator_adjusted_Jaccard_distance = SequenceInstabilityTopInfluencers("test", k + 1, AdjJaccard)
            instability_adjusted_jaccard = calculator_adjusted_Jaccard_distance.computeInstabilityOfTopKSequence(list_of_top_k_lists, pathPrefixAdjJaccard)
            instability_values_adjusted_jaccard_distance.append(instability_adjusted_jaccard)
            
            pathPrefixSFH = testDir + self._resultsFolderStructure.pathSep() + "SFH_k" + str(k+1)
            calculator_SFH_distance = SequenceInstabilityTopInfluencers_SFH("test", k + 1)
            instability_SFH = calculator_SFH_distance.computeInstabilityOfTopKSequence(list_of_top_k_lists, pathPrefixSFH)
            instability_values_SFH_distance.append(instability_SFH)
        
        distMeasureCmpPath = testDir + self._resultsFolderStructure.pathSep() + "cmp.txt"
        self.saveTable(instability_values_jaccard_distance, instability_values_adjusted_jaccard_distance, instability_values_SFH_distance, distMeasureCmpPath)
