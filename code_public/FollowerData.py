from DataReader import DataReader
from DataReader import CSVNetworkData
from Content import FollowersSurvey
from Network import Network
from shutil import copy2
import os
import numpy as np 

FOLLOWER_DATA_KEY = "FOLLOWER_DATA"

class FollowerData:
    def __init__(self, surveyFile):
        self.csvNetworkData = CSVNetworkData(surveyFile)
        n = len(self.csvNetworkData._ids)
        self._valid = True
        if n < 1:
            self._valid = False
        indices = range(n)
        adjacencyMx = list()
        for i in indices:
            row = list()
            for j in indices:
                value = self.csvNetworkData._mx[i][j]
                if (i==j or value=="NA"):
                    row.append(0)
                else:
                    row.append(int(value))
            adjacencyMx.append(row)
        self._network = Network(adjacencyMx, self.csvNetworkData._ids, True)
    
class FollowerDataReader(DataReader):
    
    def __init__(self, resultsFolderStructure):
        self._resultsFolderStructure = resultsFolderStructure
        self._contentType = FollowersSurvey()
        statFilePath =  resultsFolderStructure.rootDir() + resultsFolderStructure.pathSep() + "followerStat.txt"
        self._followerStatisticsFile = open(statFilePath, "w")
        self._followerStatisticsFile.write("Surveys: \n")
        self._students = set()
        self._classSizeList = list()
        self._classSizeListOfTurns = dict()
        self._classNumberOfTurns = dict()
        self._studentNumberOfTurns = dict()
        self._edgeNumberOfTurns = dict()
        
    def readTurn(self, turn):
        surveys = turn.getSurveyByContentType(self._contentType)
        if (len(surveys) > 0):
            survey = surveys[0]
            print("Reading survey file:", survey.surveyFile())
            self._followerStatisticsFile.write(survey.surveyFile() + "\n")
            followerData = FollowerData(survey.surveyFile())
            turn.add(FOLLOWER_DATA_KEY, followerData)
            resultFolder = self._resultsFolderStructure.turnFolderPath(turn)
            followerNetworkPlotFile = resultFolder + "followers.png"
            copy2(survey.surveyFile(), resultFolder + os.path.basename(survey.surveyFile()))
            print(followerNetworkPlotFile)
            followerData._network.plot(followerNetworkPlotFile)
            studentIDs = followerData._network.labels()
            nr_of_sturents = len(studentIDs)
            self._students.update(studentIDs)
            self._classSizeList.append(nr_of_sturents)
            turn_index = turn.index()
            l = None
            if turn_index in self._classSizeListOfTurns:
                l = self._classSizeListOfTurns.get(turn_index)
            else:
                l = list()
                self._classSizeListOfTurns[turn_index] = l
            l.append(nr_of_sturents)
            
            if turn_index in self._classNumberOfTurns:
                self._classNumberOfTurns[turn_index] = self._classNumberOfTurns[turn_index] + 1
            else:
                self._classNumberOfTurns[turn_index] = 1
             
            if turn_index in self._studentNumberOfTurns:
                self._studentNumberOfTurns[turn_index] = self._studentNumberOfTurns[turn_index] + nr_of_sturents
            else:
                self._studentNumberOfTurns[turn_index] = nr_of_sturents
            
            nr_of_edges = followerData._network.edgeNumber()
            if turn_index in self._edgeNumberOfTurns:
                self._edgeNumberOfTurns[turn_index] = self._edgeNumberOfTurns[turn_index] + nr_of_edges
            else:
                self._edgeNumberOfTurns[turn_index] = nr_of_edges
             
    
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)
        self._followerStatisticsFile.write("Students: \n")
        for studentID in self._students:
             self._followerStatisticsFile.write(studentID + "\n")
        self._followerStatisticsFile.write("Number of students = " + str(len(self._students)) + "\n")
        meanClassSize = np.mean(self._classSizeList)
        minClassSize = np.min(self._classSizeList)
        maxClassSize = np.max(self._classSizeList)
        SDClassSize = np.std(self._classSizeList)
        self._followerStatisticsFile.write("mean of class size = " + str(meanClassSize) + "\n")
        self._followerStatisticsFile.write("min of class size = " + str(minClassSize) + "\n")
        self._followerStatisticsFile.write("max of class size = " + str(maxClassSize) + "\n")
        self._followerStatisticsFile.write("SD of class size = " + str(SDClassSize) + "\n")
        self._followerStatisticsFile.write("Class sizes of turns: \n")
        turn_indices = self._classSizeListOfTurns.keys()
        for turn_index in turn_indices:
            l =  self._classSizeListOfTurns[turn_index]
            meanClassSize = np.mean(l)
            minClassSize = np.min(l)
            maxClassSize = np.max(l)
            SDClassSize = np.std(l)
            s = "Turn " + str(turn_index) + " mean: " + str(meanClassSize)
            s += " min " + str(minClassSize) + " max: " + str(maxClassSize) 
            s += " SD " + str(SDClassSize) + " \n"
            self._followerStatisticsFile.write(s)
        
        self._followerStatisticsFile.write("Number of classes: \n")
        for turn_index in turn_indices:
            n = self._classNumberOfTurns[turn_index] 
            self._followerStatisticsFile.write("Turn " + str(turn_index) + ": " + str(n) + "\n")
            
        self._followerStatisticsFile.write("\nTotal number of students: \n")
        for turn_index in turn_indices:
            n = self._studentNumberOfTurns[turn_index] 
            self._followerStatisticsFile.write("Turn " + str(turn_index) + ": " + str(n) + "\n")
        
        self._followerStatisticsFile.write("\nTotal number of nominations: \n")
        for turn_index in turn_indices:
            n = self._edgeNumberOfTurns[turn_index] 
            self._followerStatisticsFile.write("Turn " + str(turn_index) + ": " + str(n) + "\n")
        
        self._followerStatisticsFile.close()