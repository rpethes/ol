from Data import Schools, Turn, Survey
from Content import ContentTypeProviderFactory
import os

class SurveyData:
    def __init__(self, rootDir, pathSeparator, resultsDir):
        self._rootDir = rootDir
        self._pathSeparator = pathSeparator
        self._resultsDir = resultsDir
        surveyContentsFileName = self._resultsDir + "/surveyContents.txt"
        self._surveyContentsFile = open(surveyContentsFileName, "w")
    
    def readClassFolder(self, contentTypeProvider, classFolder, classID, school):
        schoolClass = school.getOrCreateSchoolClass(classID)
        turn = Turn(schoolClass, contentTypeProvider.turn())
        schoolClass.addTurn(turn)
        file_names = os.listdir(classFolder)
        for file_name in file_names:
            contentType = contentTypeProvider.getContentType(file_name)
            full_file_path = classFolder + file_name
            survey = Survey(turn, full_file_path, contentType)
            turn.addSurvey(survey)
            if contentType.name() != "unspecified":
                self._surveyContentsFile.write(full_file_path + " = " + contentType.name() + "\n")
        
    def readTurnFolder(self, contentTypeProvider, turnFolder, schools):
        folders = os.listdir(turnFolder)
        for folder in folders:
            try:
                class_id = int(folder)
                school_id = int(class_id / 1000)
                class_folder = turnFolder + folder + self._pathSeparator
                school = schools.getOrCreateSchool(school_id)
                self.readClassFolder(contentTypeProvider, class_folder, class_id, school)
            except ValueError:
                print ("Invalid folder name: " + folder)
    
    def read(self):
        schools = Schools()
        turn_folders = list(os.listdir(self._rootDir))
        turn_folders.sort()
        turn_indices = list()
        for turn_folder in turn_folders:
            index = int(turn_folder[0])
            turn_indices.append(index)
        nr_of_turns = len(turn_folders)
        contentTypeProviderFactory = ContentTypeProviderFactory()
        for i in range(nr_of_turns):
            contentTypeProvider = contentTypeProviderFactory.create(turn_indices[i])
            folder = self._rootDir + turn_folders[i] + self._pathSeparator
            self.readTurnFolder(contentTypeProvider, folder, schools)
        self._surveyContentsFile.close()
        return schools