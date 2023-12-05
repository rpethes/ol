import shutil, os

class ResultsFolderStructure:
    def __init__(self, rootDir, pathSep):
        self._rootDir = rootDir
        self._pathSep = pathSep
        self._baseDir = rootDir + "details" + self._pathSep
        self._ecdfDir = rootDir + "ecdf" + self._pathSep
        self._instTestDir = rootDir + "instabilityMeasureTest" + self._pathSep
        shutil.rmtree(self._baseDir, ignore_errors = True)
        shutil.rmtree(self._ecdfDir, ignore_errors = True)
        shutil.rmtree(self._instTestDir, ignore_errors = True)
    
    def ecdfDir(self):
        return self._ecdfDir
    
    def instabilityTestDir(self):
        return self._instTestDir
    
    def schoolFolderPath(self, school):
        path = self._baseDir + str(school.id()) + self._pathSep
        return path
    
    def schoolClassFolderPath(self, schoolClass):
        parent = schoolClass.parent()
        path = self.schoolFolderPath(parent) + str(schoolClass.id()) + self._pathSep
        return path
    
    def turnFolderPath(self, turn):
        parent = turn.parent()
        path = self.schoolClassFolderPath(parent) + str(turn.index()) + self._pathSep
        return path
    
    def buildSchoolClassFolders(self, schoolClass, folder):
        os.mkdir(folder)
        turns = schoolClass.turns()
        for turn in turns:
            folderPath = self.turnFolderPath(turn)
            os.mkdir(folderPath)
    
    def buildSchoolFolders(self, school, folder):
        os.mkdir(folder)
        classes = school.classes()
        for schoolClass in classes:
            folderPath = self.schoolClassFolderPath(schoolClass)
            self.buildSchoolClassFolders(schoolClass, folderPath)
            
    def pathSep(self):
        return self._pathSep
    
    def rootDir(self):
        return self._rootDir
        
    def build(self, schools):
        os.mkdir(self._baseDir)
        os.mkdir(self._ecdfDir)
        os.mkdir(self._instTestDir)
        schoolList = schools.schools()
        for school in schoolList:
            folder = self.schoolFolderPath(school)
            self.buildSchoolFolders(school, folder)
            