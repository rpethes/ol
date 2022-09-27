from Content import FollowersSurvey, FriendsSurvey
from Utils import save_bar

class SurveyStatistics:
    def __init__(self, targetFolder):
        self._targetFolder = targetFolder
    
    def processScoolClass(self, schoolClass):
        turns = schoolClass.turns()
        followerInTurns = list()
        friensInTurns = list()
        followersSurvey = FollowersSurvey()
        friendsSurvey = FriendsSurvey()
        for turn in turns:
            l = turn.getSurveyByContentType(followersSurvey)
            if (len(l) > 0):
                followerInTurns.append(turn.index())
                self._sum_of_followerSurveys = self._sum_of_followerSurveys + 1
            l = turn.getSurveyByContentType(friendsSurvey)
            if (len(l) > 0):
                friensInTurns.append(turn.index())
                self._sum_of_friendsSurveys = self._sum_of_friendsSurveys + 1
        
        nFollowerInTurns = len(followerInTurns)
        nFriensInTurns = len(friensInTurns)
        
        self._follower_histogram[nFollowerInTurns] = self._follower_histogram[nFollowerInTurns] + 1 
        self._friends_histogram[nFriensInTurns] = self._friends_histogram[nFriensInTurns] + 1
        strFollowerInTurns = " ,".join(str(x) for x in followerInTurns) 
        strFriensInTurns = " ,".join(str(x) for x in friensInTurns)
        self._surveyStatistics.write(str(schoolClass.id()) + ";" + str(schoolClass.parent().id()) + ";" + strFollowerInTurns + ";" + strFriensInTurns + "\n")
        if nFollowerInTurns < 4:
            self._follower_less_than_four.append(schoolClass.id())
        if nFriensInTurns < 4:
            self._friends_less_than_four.append(schoolClass.id())
            
    def processSchool(self, school):
        classes = school.classes()
        self._nr_of_classes = self._nr_of_classes + len(classes)
        for schoolClass in classes:
            self.processScoolClass(schoolClass)
        
    def buildStatistics(self, schools):
        self._surveyStatistics = open(self._targetFolder + "surveyStat.csv", "w")
        self._surveyStatistics.write("class;school;followers;friends\n")
        self._sum_of_followerSurveys = 0
        self._sum_of_friendsSurveys = 0
        self._nr_of_classes = 0
        self._follower_histogram = [0,0,0,0,0,0]
        self._friends_histogram = [0,0,0,0,0,0]
        self._friends_less_than_four = []
        self._follower_less_than_four = []
        schoolList = schools.schools()
        for school in schoolList:
            self.processSchool(school)    
        self._surveyStatistics.close()
        
        summary = open(self._targetFolder + "surveySummary.csv", "w")
        summary.write("nr of schools = " + str(len(schools.schools())) + "\n")
        summary.write("nr of classes = " + str(self._nr_of_classes) + "\n")
        summary.write("nr of follower terms = " + str(self._sum_of_followerSurveys) + "\n")
        summary.write("nr of friends terms = " + str(self._sum_of_friendsSurveys) + "\n")
        summary.write("follower histrogram = " + str(self._follower_histogram) + "\n")
        summary.write("friends histrogram = " + str(self._friends_histogram) + "\n")
        summary.write("follower less then 4 waves = " + str(self._follower_less_than_four) + "\n")
        summary.write("friends less then 4 waves = " + str(self._friends_less_than_four) + "\n")
        summary.close()
        save_bar(self._targetFolder + "followerTurnesHistogram.png", [0,1,2,3,4,5], self._follower_histogram, ['0','1','2','3','4','5'] )
        save_bar(self._targetFolder + "frindesTurnesHistogram.png", [0,1,2,3,4,5], self._friends_histogram, ['0','1','2','3','4','5'] )