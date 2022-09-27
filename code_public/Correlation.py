from DataReader import DataReader
import numpy
import scipy.stats
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

class Correlation(DataReader):
    def __init__(self, name,  resultsFolderStructure, resultsDir, metricsRows, metricsCols):
        self._name = name
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._metricsRows = metricsRows
        self._metricsCols = metricsCols
        
    
    def createHeatMap(self, mx, targetFilePath, xlabels, ylabels, labelX, labelY):
        # Colors
        cmap = sb.diverging_palette(500, 10, as_cmap=True)
        cbar = len(xlabels) > 1 and len(ylabels) > 1
        hm = None
        if len(ylabels) == 1:
            #annot_kws= {'rotation':"vertical"}
            plt.figure(figsize=(15, 2))
            hm = sb.heatmap(mx, cmap=cmap, annot=True,  xticklabels = xlabels, yticklabels = ylabels, vmax= 1.0, cbar = cbar)
        else:
            hm = sb.heatmap(mx, cmap=cmap, annot=True,  xticklabels = xlabels, yticklabels = ylabels, vmax= 1.0, cbar = cbar)
        figure = hm.get_figure()    
        if labelX != None and len(ylabels) > 1:
            plt.xlabel(labelX, fontweight='normal', fontsize=12)
            #figure.set_xlabel(labelX)
        
        if labelY != None:
            plt.ylabel(labelY, fontweight='normal', fontsize=12)
            #figure.set_xlabel(labelY)
        
        #if len(ylabels) == 1:
            #bottom, top = hm.get_ylim()
            #hm.set_ylim(bottom, top - 0.5)
            #plt.gcf().set_size_inches(15, 4)
            #s = plt.gcf().get_size_inches()
            #plt.gcf().set_size_inches(s[0], (s[0] / len(xlabels)))
        figure.savefig(targetFilePath)
        plt.close()
      
    def processData(self, turn, rowMetricDataObj, colMetricDataObj):
        pass
    
    def readTurn(self, turn):
        for rowMetric in self._metricsRows:
            rowMetricKey = rowMetric.unique_name()
            if turn.hasKey(rowMetricKey) == False:
                continue
            rowMetricData = turn.get(rowMetricKey)
            for colMetric in self._metricsCols:
                colMetricKey = colMetric.unique_name()
                if turn.hasKey(colMetricKey) == False:
                    continue
                colMetricData = turn.get(colMetricKey)
                self.processData(turn, rowMetricData, colMetricData)
        
    def postProcess(self, schools):
        pass
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self.postProcess(schools)
               
class CentralityValueCorrelation(Correlation):
    def __init__(self, name,  resultsFolderStructure, resultsDir, metricsRows, metricsCols):
        Correlation.__init__(self, name, resultsFolderStructure, resultsDir, metricsRows, metricsCols)
        self._valuesX = dict()
        self._valuesY = dict()
        
    def processData(self, turn, rowMetricDataObj, colMetricDataObj):
        rowIDToValueDict = rowMetricDataObj.idToValueDict()
        colIDToValueDict = colMetricDataObj.idToValueDict()
        rowIDList = rowMetricDataObj.idsList()
        colIDList = colMetricDataObj.idsList()
        common_id_list = set(rowIDList) & set(colIDList)
        x = []
        y = []
        for ID in common_id_list:
            x.append(rowIDToValueDict[ID])
            y.append(colIDToValueDict[ID])
        key = rowMetricDataObj.unique_name() + ":" + colMetricDataObj.unique_name()
        XList = None
        YList = None
        if self._valuesX.has_key(key):
            XList = self._valuesX.get(key)
        else:
            XList = []
            self._valuesX[key] = XList
        
        if self._valuesY.has_key(key):
            YList = self._valuesY.get(key)
        else:
            YList = []
            self._valuesY[key] = YList
        XList.extend(x)
        YList.extend(y)
        
    def postProcess(self, schools):
        statFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".txt"
        f = open(statFilePath, "w")
        keys = self._valuesX.keys()
        for key in keys:
            x = self._valuesX[key]
            y = self._valuesY[key]
            r, p = scipy.stats.pearsonr(x, y)
            f.write(key + " correlation = " + str(r) + " p-value =" + str(p) + "\n")
        f.close()
            
            
class CentralityRankCorrelation(Correlation):
    def __init__(self, name,  resultsFolderStructure, resultsDir, metricsRows, metricsCols):
        Correlation.__init__(self, name, resultsFolderStructure, resultsDir, metricsRows, metricsCols)
        self._valuesX = dict()
        self._valuesY = dict()
    
    def computeRestrictedList(self, sortedValueListRow, common_id_set):
        restrictedList = []
        for item in sortedValueListRow:
            l = []
            for ID in item:
                if ID in common_id_set:
                    l.append(ID)
            if len(l) > 0:
                restrictedList.append(l)
        return restrictedList
    
    def computeRankMap(self, sortedValueList):
        rankMap = dict()
        rank = 0
        for item in sortedValueList:
            rank = rank + len(item)
            for ID in item:
                rankMap[ID] = rank
            rank = rank + 1
        return rankMap
    
    def processData(self, turn, rowMetricDataObj, colMetricDataObj):   
        rowIDList = rowMetricDataObj.idsList()
        colIDList = colMetricDataObj.idsList()
        common_id_set = set(rowIDList) & set(colIDList)
        sortedValueListRow = rowMetricDataObj.idsListOfSortedValues()
        rowRestrictedList = self.computeRestrictedList(sortedValueListRow, common_id_set)
        sortedValueListCol = colMetricDataObj.idsListOfSortedValues()
        colRestrictedList = self.computeRestrictedList(sortedValueListCol, common_id_set)
        rowRankMap = self.computeRankMap(rowRestrictedList)
        colRankMap = self.computeRankMap(colRestrictedList)
        x = []
        y = []
        n = len(common_id_set)
        for ID in common_id_set:
            x.append(float(rowRankMap[ID]) / n)
            y.append(float(colRankMap[ID]) / n)
        key = rowMetricDataObj.unique_name() + ":" + colMetricDataObj.unique_name()
        XList = None
        YList = None
        if self._valuesX.has_key(key):
            XList = self._valuesX.get(key)
        else:
            XList = []
            self._valuesX[key] = XList
        
        if self._valuesY.has_key(key):
            YList = self._valuesY.get(key)
        else:
            YList = []
            self._valuesY[key] = YList
        XList.extend(x)
        YList.extend(y)
        
    def postProcess(self, schools):
        statFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".txt"
        f = open(statFilePath, "w")
        keys = self._valuesX.keys()
        for key in keys:
            x = self._valuesX[key]
            y = self._valuesY[key]
            r, p = scipy.stats.pearsonr(x, y)
            f.write(key + " correlation = " + str(r) + " p-value =" + str(p) + "\n")
        f.close()
        
        
class KendallTauCorrelation(Correlation):
    def __init__(self, name,  resultsFolderStructure, resultsDir, metricsRows, metricsCols, rowNames, colNames,  xlabel, ylabel):
        Correlation.__init__(self, name, resultsFolderStructure, resultsDir, metricsRows, metricsCols)
        self._correlationValues = dict()
        self._rowNames = rowNames
        self._colNames = colNames
        self._xlabel = xlabel
        self._ylabel = ylabel
        
    def processData(self, turn, rowMetricDataObj, colMetricDataObj):   
        rowIDList = rowMetricDataObj.idsList()
        colIDList = colMetricDataObj.idsList()
        common_id_set = set(rowIDList) & set(colIDList)
        rowIDtoValue = rowMetricDataObj.idToValueDict()
        colIDtoValue = colMetricDataObj.idToValueDict()
        row_values = []
        col_values = []
        for student_id in common_id_set:
            row_values.append(rowIDtoValue[student_id])
            col_values.append(colIDtoValue[student_id])
        tau, p_value = scipy.stats.kendalltau(row_values, col_values)
        if numpy.isnan(tau):
            return
        key = rowMetricDataObj.unique_name() + "#" + colMetricDataObj.unique_name()
        tau_values = None
        if key in self._correlationValues:
            tau_values = self._correlationValues[key]
        else:
            tau_values = []
            self._correlationValues[key] = tau_values
        tau_values.append(tau)
       
    def postProcess(self, schools):
        statFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".txt"
        f = open(statFilePath, "w")
        nRows = len(self._metricsRows)
        nCols = len(self._metricsCols)
        mx = np.empty((nRows, nCols))
        mx[:] = np.nan
        min_variance = 100
        max_variance = -1.0
        row_index = 0
        for rowMetric in self._metricsRows:
            rowMetricKey = rowMetric.unique_name()
            col_index = 0
            for colMetric in self._metricsCols:
                colMetricKey = colMetric.unique_name()
                key = rowMetricKey + "#" + colMetricKey
                values = self._correlationValues[key]
                m = numpy.mean(values)
                var  = numpy.var(values)
                mx[(row_index, col_index)] = m
                col_index = col_index + 1
                f.write(key + " mean = " + str(m) + " variance =" + str(var) + "\n")
                if var > 1e-12:
                    min_variance = min([min_variance, var])
                    max_variance = max([max_variance, var]) 
            row_index = row_index + 1
        f.write("min_variance = " + str(min_variance) + "\n")
        f.write("max_variance = " + str(max_variance))
        f.close()
        plotFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".png"
        self.createHeatMap(mx, plotFilePath, self._colNames, self._rowNames, self._xlabel, self._ylabel)
        
        
class JaccardTopInfluencersSimilarity(Correlation):
    def __init__(self, name, n,  resultsFolderStructure, resultsDir, metricsRows, metricsCols, rowNames, colNames,  xlabel, ylabel ):
        Correlation.__init__(self, name, resultsFolderStructure, resultsDir, metricsRows, metricsCols)
        self._n = n
        self._values = dict()
        self._rowNames = rowNames
        self._colNames = colNames
        self._xlabel = xlabel
        self._ylabel = ylabel
    
    def getTopInfluencers(self, metricDataObj, common_id_set):
        idsListOfSortedValues = metricDataObj.idsListOfSortedValues()
        topInfluencers = []
        for idList in idsListOfSortedValues:
            for ID in idList:
                if ID in common_id_set:
                    topInfluencers.append(ID)
            if len(topInfluencers) >= self._n:
                break
        return topInfluencers
    
    def jaccard(self, list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        intersection = set.intersection(s1, s2)
        uni = set.union(s1, s2)
        ret = float(len(intersection)) / float(len(uni))
        return ret
    
    def processData(self, turn, rowMetricDataObj, colMetricDataObj):   
        rowIDList = rowMetricDataObj.idsList()
        colIDList = colMetricDataObj.idsList()
        common_id_set = set(rowIDList) & set(colIDList)
        topInfluencersRow = self.getTopInfluencers(rowMetricDataObj, common_id_set)
        topInfluencersCol = self.getTopInfluencers(colMetricDataObj, common_id_set)
        jaccardSimiarityValue = self.jaccard(topInfluencersRow, topInfluencersCol)
        
        key = rowMetricDataObj.unique_name() + "#" + colMetricDataObj.unique_name()
        values = None
        if key in self._values:
            values = self._values[key]
        else:
            values = []
            self._values[key] = values
        values.append(jaccardSimiarityValue)
        return jaccardSimiarityValue
        
    def postProcess(self, schools):
        statFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".txt"
        f = open(statFilePath, "w")
        nRows = len(self._metricsRows)
        nCols = len(self._metricsCols)
        mx = np.empty((nRows, nCols))
        mx[:] = np.nan
        min_variance = 100
        max_variance = -1.0
        row_index = 0
        for rowMetric in self._metricsRows:
            rowMetricKey = rowMetric.unique_name()
            col_index = 0
            for colMetric in self._metricsCols:
                colMetricKey = colMetric.unique_name()
                key = rowMetricKey + "#" + colMetricKey
                values = self._values[key]
                m = numpy.mean(values)
                var  = numpy.var(values)
                mx[(row_index, col_index)] = m
                col_index = col_index + 1
                f.write(key + " mean = " + str(m) + " variance =" + str(var) + "\n")
                if var > 1e-12:
                    min_variance = min([min_variance, var])
                    max_variance = max([max_variance, var]) 
            row_index = row_index + 1
        f.write("min_variance = " + str(min_variance) + "\n")
        f.write("max_variance = " + str(max_variance))
        f.close()
        plotFilePath =  self._resultsFolderStructure.rootDir() + self._resultsFolderStructure.pathSep() + self._name + ".png"
        self.createHeatMap(mx, plotFilePath,self._colNames,  self._rowNames, self._xlabel, self._ylabel)