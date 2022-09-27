from UserData import UserData
class Survey:
    def __init__(self, parent, surveyFile, contentType):
        self._parent = parent
        self._surveyFile = surveyFile
        self._contentType = contentType
        
    def surveyFile(self):
        return self._surveyFile
    
    def contentType(self):
        return self._contentType
    
    def parent(self):
        return self._parent
    
class Turn(UserData):
    def __init__(self, parent, index):
        UserData.__init__(self)
        self._parent = parent
        self._index = index
        self._surveysDict = dict()
        self._surveys = list()
        
    def parent(self):
        return self._parent
    
    def index(self):
        return self._index
    
    def surveys(self):
        return self._surveys
    
    def addSurvey(self, survey):
        self._surveys.append(survey)
        contentType = survey.contentType()
        list_of_contenttype = None
        contentTypeName = contentType.name()
        if (contentTypeName in self._surveysDict.keys()):
            list_of_contenttype =  self._surveysDict[contentTypeName]
        else:
            list_of_contenttype = list()
            self._surveysDict[contentTypeName] = list_of_contenttype 
        list_of_contenttype.append(survey)
        
    def getSurveyByContentType(self, contentType):
        contentTypeName = contentType.name()
        if (contentTypeName in self._surveysDict.keys() ):
            return self._surveysDict[contentTypeName]
        return list()

class SchoolClass(UserData):
    def __init__(self, parent, classID):
        UserData.__init__(self)
        self._parent = parent
        self._id = classID
        self._turnsDict = dict()
        
    def parent(self):
        return self._parent
    
    def id(self):
        return self._id
    
    def turns(self):
        return self._turnsDict.values()
    
    def turnsWithUserData(self, key):
        turnObjects = self.turns()
        turnObjectsHasKey = []
        for turnObject in turnObjects:
            if turnObject.hasKey(key):
                turnObjectsHasKey.append(turnObject)
        return turnObjectsHasKey
                
    def addTurn(self, turn):
        turn_index = turn.index()
        self._turnsDict[turn_index] = turn
        
    def turnIndices(self):
        return self._turnsDict.keys()
    
    def isValidTurnIndex(self, index):
        return(index in self._turnsDict.keys())
    
class School:
    def __init__(self, schoolID):
        self._id = schoolID
        self._classesDict = dict()
        
    def id(self):
        return self._id
    
    def classes(self):
        return self._classesDict.values()
    
    def addClass(self, oneClass):
        classID = oneClass.id()
        self._classesDict[classID] = oneClass
        
    def classIDs(self):
        return self._classesDict.keys()
    
    def getOrCreateSchoolClass(self, classID):
        if (classID in self._classesDict.keys()):
            return self._classesDict[classID]
        schoolClass = SchoolClass(self, classID)
        self._classesDict[classID] = schoolClass
        return schoolClass
        
    
class Schools:
    def __init__(self):
        self._schoolsDict = dict()
    
    def addSchool(self, school):
        schoolID = school.id()
        self._schoolsDict[schoolID] = school
        
    def schools(self):
        return self._schoolsDict.values()
    
    def schoolIDs(self):
        return self._schoolsDict.keys()
    
    def getSchool(self, schoolID):
        return self._schoolsDict[schoolID]
    
    def isValidSchoolID(self, schoolID):
        return (schoolID in self._schoolsDict.keys())
    
    def getOrCreateSchool(self, schoolID):
        if self.isValidSchoolID(schoolID):
            return self.getSchool(schoolID)
        school = School(schoolID)
        self.addSchool(school)
        return school