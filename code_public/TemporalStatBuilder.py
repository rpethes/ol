from DataReader import DataReader

class TemporalStatBuilder(DataReader):
    def __init__(self, name, target_user_data_key, prefix, resultsFolderStructure, resultsDir):
        self._name = name
        self._target_user_data_key = target_user_data_key
        self._prefix = prefix
        self._resultsFolderStructure = resultsFolderStructure
        self._resultsDir = resultsDir
        
    
    def getDataFrom(self, src, key):
        userData = src.get(self._target_user_data_key)
        if userData == None:
            return None
        data = userData.get(key)
        return data
    
    def processData(self, data, schoolClass):
        pass
    
    def readSchoolClass(self, schoolClass):
        data = self.getDataFrom(schoolClass, self._name)
        if data != None:
            self.processData(data, schoolClass)
            
    def buildStatistics(self, schools):
        pass
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self.buildStatistics(schools)