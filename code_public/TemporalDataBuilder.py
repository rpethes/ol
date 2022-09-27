from DataReader import DataReader
from UserData import UserData
FOLLOWER_TEMPORAL_DATA_KEY = "FOLLOWER_TEMPORAL_DATA"
FRIEND_TEMPORAL_DATA_KEY = "FRIEND_TEMPORAL_DATA"
AGGR_TEMPORAL_DATA_KEY = "AGGR_TEMPORAL_DATA"

class TemporalDataBuilder(DataReader):
    def __init__(self, name, target_user_data_key, resultsFolderStructure, resultsDir, minimum_number_of_turns):
        self._name = name
        self._target_user_data_key = target_user_data_key
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        self._calculators = []
        self._calculator_summary_files = dict()
        self._calculator_summary_file_names = dict()
        self._minimum_number_of_turns = minimum_number_of_turns
        
    def registerCalculator(self, calculator):
        self._calculators.append(calculator)
        calculatorFileName = self._resultsDir + "/" + self._name + "_" + calculator.fullName() + ".txt"
        f = open(calculatorFileName, "w")
        self._calculator_summary_files[calculator.fullName()] = f
        self._calculator_summary_file_names[calculator.fullName()] = calculatorFileName
    
    def getOpinionLeaderMetric(self, turn, metric_name):
        key = self._name + "_" + metric_name
        metric_data = turn.get(key)
        return metric_data
    
    def addResultTo(self, target, key, data):
        targetUserData = target.get(self._target_user_data_key)
        if targetUserData == None:
            targetUserData = UserData()
            target.add(self._target_user_data_key, targetUserData)
        targetUserData.add(key, data)
             
    def execute(self, schoolClass, resultFolder, calculator, turnsList, opinionLeaderMetricDataList):
        result = calculator.calc(schoolClass, turnsList, opinionLeaderMetricDataList)
        self.addResultTo(schoolClass, calculator.fullName(), result)
        s = str(result)
        result.writeToFile(resultFolder)
        f = self._calculator_summary_files[calculator.fullName()]
        f.write(s)
    
    def readSchoolClass(self, schoolClass):
        turns = schoolClass.turns()
        print("schoolClass: " + str(schoolClass.id()))
        resultFolder = self._resultsFolderStructure.schoolClassFolderPath(schoolClass)
        for calculator in self._calculators:
            turnsList = list()
            opinionLeaderMetricDataList = list()
            metric_name = calculator.metricName()
            for turn in turns:
                opinionLeaderMetric = self.getOpinionLeaderMetric(turn, metric_name)
                if opinionLeaderMetric != None:
                    turnsList.append(turn)
                    opinionLeaderMetricDataList.append(opinionLeaderMetric)
            if len(turnsList) >= self._minimum_number_of_turns:
                self.execute(schoolClass,resultFolder, calculator, turnsList, opinionLeaderMetricDataList)
                
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)           
        for calculator in self._calculators:
            f = self._calculator_summary_files[calculator.fullName()]
            summaryFilePath = self._calculator_summary_file_names[calculator.fullName()]
            f.flush()
            f.close()
            calculator.createSummaryPlot(summaryFilePath)
    
    def calculators(self):
        return self._calculators
    
class FollowerTemporalDataBuilder(TemporalDataBuilder):
    
    def __init__(self, resultsFolderStructure, resultsDir, minimum_number_of_turns):
        TemporalDataBuilder.__init__(self, "follower", FOLLOWER_TEMPORAL_DATA_KEY, resultsFolderStructure, resultsDir, minimum_number_of_turns)
        
class FriendsTemporalDataBuilder(TemporalDataBuilder):
    
    def __init__(self, resultsFolderStructure, resultsDir, minimum_number_of_turns):
        TemporalDataBuilder.__init__(self, "friend", FRIEND_TEMPORAL_DATA_KEY, resultsFolderStructure, resultsDir, minimum_number_of_turns)
        
class AggrTemporalDataBuilder(TemporalDataBuilder):
    
    def __init__(self, resultsFolderStructure, resultsDir, minimum_number_of_turns):
        TemporalDataBuilder.__init__(self, "aggr", AGGR_TEMPORAL_DATA_KEY, resultsFolderStructure, resultsDir, minimum_number_of_turns)
