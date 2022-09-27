from DataReader import DataReader
import matplotlib.pyplot as plt
import numpy as np

class SequenceInstabilityPlot(DataReader):
    def __init__(self, key_name_pairs, xlabel, ylabel, resultsFolderStructure, resultsDir, targetFileName):
        self._key_name_pairs = key_name_pairs
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._targetFileName = targetFileName
        self._valueDict_len4 = dict()
        self._valueDict_len5 = dict()
        
    
    def getDataFrom(self, src, user_data_key, metric_name):
        userData = src.get(user_data_key)
        if userData == None:
            return None
        data = userData.get(metric_name)
        return data
    
    def create_key(self, user_data_key, metric_name):
        key = user_data_key + metric_name
        return key
    
    def processData(self, user_data_key, metric_name, data, schoolClass):
        sequenceLen = data.getSequenceLen()
        valueDict = None 
        if sequenceLen == 4:
            valueDict = self._valueDict_len4
        elif sequenceLen == 5:
            valueDict = self._valueDict_len5
        
        key = self.create_key(user_data_key, metric_name)
        values_list = valueDict.get(key, None)
        if values_list == None:
            values_list = []
            valueDict[key] = values_list
        value = data.getValue()
        values_list.append(value)
    
    def readSchoolClass(self, schoolClass):
        for key_name_pair in self._key_name_pairs:
            user_data_key = key_name_pair[0]
            metric_name = key_name_pair[1]
            data = self.getDataFrom(schoolClass, user_data_key, metric_name)
            if data != None:
                self.processData(user_data_key, metric_name, data, schoolClass)
            
    def createPlot(self, schools):
        value_lists_len4 = []
        value_lists_len5 = []
        names_len4 = []
        names_len5 = []
        xs_len4 = []
        xs_len5 = []
        colors_len4 = []
        colors_len5 = []
        index_len4= 1
        index_len5= 1
        for key_name_pair in self._key_name_pairs:
            user_data_key = key_name_pair[0]
            metric_name = key_name_pair[1]
            display_name = key_name_pair[2]
            display_color = key_name_pair[3]
           
            key = self.create_key(user_data_key, metric_name)
            values_len4 = self._valueDict_len4.get(key, None)
            if (values_len4 != None):
                value_lists_len4.append(values_len4) 
                names_len4.append(display_name)
                xs_len4.append(np.random.normal(index_len4, 0.04, len(values_len4)))
                colors_len4.append(display_color)
                index_len4 = index_len4 + 1
            
            values_len5 = self._valueDict_len5.get(key, None)
            if (values_len5 != None):
                value_lists_len5.append(values_len5) 
                names_len5.append(display_name)
                xs_len5.append(np.random.normal(index_len5, 0.04, len(values_len5)))
                colors_len5.append(display_color)
                index_len5 = index_len5 + 1
        
        boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
        flierprops = dict(marker='o', markersize=1, linestyle='none')
        whiskerprops = dict(color='#00145A')
        capprops = dict(color='#00145A')
        medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
        
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        fig.subplots_adjust(hspace=.5)
        bplot1 = ax1.boxplot(value_lists_len4, labels=names_len4, notch=False, boxprops=boxprops,
        whiskerprops=whiskerprops,capprops=capprops, flierprops=flierprops,
        medianprops=medianprops,showmeans=False)
        
        ax1.set_xlabel("Sequence length = 4")
        
        bplot2 = ax2.boxplot(value_lists_len5, labels=names_len5, notch=False, boxprops=boxprops,
        whiskerprops=whiskerprops,capprops=capprops, flierprops=flierprops,
        medianprops=medianprops,showmeans=False)
        ax2.set_xlabel("Sequence length = 5")
        for x, val, c in zip(xs_len4, value_lists_len4, colors_len4):
            ax1.scatter(x, val, alpha=0.4, color=c)
            
        for x, val, c in zip(xs_len5, value_lists_len5, colors_len5):
            ax2.scatter(x, val, alpha=0.4, color=c)
            
        #plt.xlabel(self._xlabel, fontweight='normal', fontsize=14)
        #plt.ylabel(self._ylabel, fontweight='normal', fontsize=14)
        
        # common labels
        
        fig.supylabel(self._ylabel)
        filename =  self._resultsDir + self._targetFileName
        plt.savefig(filename)
        plt.close()
        """
        value_lists = []
        names = []
        xs = []
        colors = []
        index = 1
        for key_name_pair in self._key_name_pairs:
            user_data_key = key_name_pair[0]
            metric_name = key_name_pair[1]
            display_name = key_name_pair[2]
            display_color = key_name_pair[3]
           
            key = self.create_key(user_data_key, metric_name)
            values = self._valueDict.get(key, None)
            if (values != None):
                value_lists.append(values) 
                names.append(display_name)
                xs.append(np.random.normal(index, 0.04, len(values)))
                colors.append(display_color)
                index = index + 1
        
        boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
        flierprops = dict(marker='o', markersize=1, linestyle='none')
        whiskerprops = dict(color='#00145A')
        capprops = dict(color='#00145A')
        medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
        
        plt.boxplot(value_lists, labels=names, notch=False, boxprops=boxprops,
        whiskerprops=whiskerprops,capprops=capprops, flierprops=flierprops,
        medianprops=medianprops,showmeans=False)
        
        plt.xlabel(self._xlabel, fontweight='normal', fontsize=14)
        plt.ylabel(self._ylabel, fontweight='normal', fontsize=14)
        for x, val, c in zip(xs, value_lists, colors):
            plt.scatter(x, val, alpha=0.4, color=c)
    
        filename =  self._resultsDir + self._targetFileName
        plt.savefig(filename)
        plt.close()
        """
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self.createPlot(schools)