class ContentType:
    def __init__(self):
        self._name = "unspecified"
        self._description = ""
    
    def name(self):
        return self._name
    
    def description(self):
        return self._description
    
class FollowersSurvey(ContentType):
    def __init__(self):
        self._name = "followers"
        self._description = "Survey of followers of a class"
        
class FriendsSurvey(ContentType):
    def __init__(self):
        self._name = "friends"
        self._description = "Survey of friends of a class"
        
class SurveyFile:
    def __init__(self, fileName):
        self._fileName = fileName
        dotSeperatedParts = fileName.split(".")
        if (len(dotSeperatedParts) != 2):
            raise ValueError("SurveyFileName: the input filename has invalid format:" + fileName)
        ext = ""
        if (len(dotSeperatedParts) > 1):
            ext = dotSeperatedParts[-1]
        self._ext = ext
        name = dotSeperatedParts[0]
        nameParts = name.split("_")
        if (len(nameParts) < 4):
            raise ValueError("SurveyFileName: the input filename has invalid format:" + fileName)
        self._nameParts = nameParts
        
    def ext(self):
        return self._ext
    
    def parts(self):
        return self._nameParts
    
    def fileName(self):
        return self._fileName
    
    
class ContentTypeProvider:
    def __init__(self, turn):
        self._turn = turn
    
    def turn(self):
        return self._turn
    
    def turnDependentContentType(self, parts):
        raise NotImplementedError("ContentTypeProvider.turnDependentContentType is not implemented")
    
    def getValidSurveyFolders(self):
        raise NotImplementedError("ContentTypeProvider.getValidSurveyFolders is not implemented")
    
    
    def getContentType(self, fileName):
        try:
            surveyFile = SurveyFile(fileName)
            parts = surveyFile.parts()
            return self.turnDependentContentType(parts)
        except ValueError as err:
            print(str(err))
        unknownContentType = ContentType()
        return unknownContentType


class FileNameBasedContentTypeProvider(ContentTypeProvider):
    def getContentType(self, fileName):
        if fileName == "advice_seeking.csv":
            return FollowersSurvey()
        
        if fileName == "friends.csv":
            return FriendsSurvey()
    
        return ContentType()  
        
class ContentTypeProviderTurn1(ContentTypeProvider):
    def turnDependentContentType(self, parts):
        if (len(parts)==4 and parts[1]=="10" and parts[2]=="4" and parts[3]=="1"):
            return FollowersSurvey()
        if (len(parts)==5 and parts[1]=="14" and parts[2]=="1" and parts[3]=="1" and parts[4]=="barat"):
            return FriendsSurvey()
        return ContentType()
    
    def getValidSurveyFolders(self):
        surveyFolders = set()
        surveyFolders.add("10")
        surveyFolders.add("14")
        return surveyFolders

class ContentTypeProviderTurn2(ContentTypeProvider):
    def turnDependentContentType(self, parts):
        if (len(parts)==4 and parts[1]=="10" and parts[2]=="4" and parts[3]=="2"):
            return FollowersSurvey()
        if (len(parts)==5 and parts[1]=="16" and parts[2]=="1" and parts[3]=="2" and parts[4]=="barat"):
            return FriendsSurvey()
        return ContentType()
    
    def getValidSurveyFolders(self):
        surveyFolders = set()
        surveyFolders.add("10")
        surveyFolders.add("16")
        return surveyFolders
    
class ContentTypeProviderTurn3(ContentTypeProvider):
    def turnDependentContentType(self, parts):
        if (len(parts)==4 and parts[1]=="17" and parts[2]=="4" and parts[3]=="3"):
            return FollowersSurvey()
        if (len(parts)==5 and parts[1]=="18" and parts[2]=="1" and parts[3]=="3" and parts[4]=="barat"):
            return FriendsSurvey()
        return ContentType()
    
    def getValidSurveyFolders(self):
        surveyFolders = set()
        surveyFolders.add("17")
        surveyFolders.add("18")
        return surveyFolders
    
    
class ContentTypeProviderTurn4(ContentTypeProvider):
    def turnDependentContentType(self, parts):
        if (len(parts)==4 and parts[1]=="19" and parts[2]=="4" and parts[3]=="4"):
            return FollowersSurvey()
        if (len(parts)==5 and parts[1]=="20" and parts[2]=="1" and parts[3]=="4" and parts[4]=="barat"):
            return FriendsSurvey()
        return ContentType()
    
    def getValidSurveyFolders(self):
        surveyFolders = set()
        surveyFolders.add("19")
        surveyFolders.add("20")
        return surveyFolders
    
    
class ContentTypeProviderTurn5(ContentTypeProvider):
    def turnDependentContentType(self, parts):
        if (len(parts)==4 and parts[1]=="18" and parts[2]=="4" and parts[3]=="5"):
            return FollowersSurvey()
        if (len(parts)==5 and parts[1]=="19" and parts[2]=="1" and parts[3]=="5" and parts[4]=="barat"):
            return FriendsSurvey()
        return ContentType()
    
    def getValidSurveyFolders(self):
        surveyFolders = set()
        surveyFolders.add("18")
        surveyFolders.add("19")
        return surveyFolders
    
class ContentTypeProviderFactory:
    def create(self, turn):
        return FileNameBasedContentTypeProvider(turn)