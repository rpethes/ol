import csv

class CSVNetworkData:
    def read(self):
        with open(self._csvfile) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            header = next(csvreader)
            self._ids = header[1:]
            self._mx = list() 
            for row in csvreader:
                self._mx.append(row[1:])
            
    def __init__(self, csvfile):
        self._csvfile = csvfile
        self.read()


class DataReader:  
    def readTurn(self, turn):
        pass
    
    def readSchoolClass(self, schoolClass):
        turns = schoolClass.turns()
        for turn in turns:
            self.readTurn(turn)
        
    def readSchool(self, school):
        classes = school.classes()
        for schoolClass in classes:
            self.readSchoolClass(schoolClass)
            
    def read(self, schools):
        schoolList = schools.schools()
        for school in schoolList:
            self.readSchool(school)