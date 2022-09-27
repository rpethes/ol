
class SequenceInstabilityStatsTableRow:
    def __init__(self, name_, follower_stat_, friends_stat_):
        self.name = name_
        self.follower_stat = follower_stat_
        self.friends_stat = friends_stat_

class SequenceInstabilityStatsTableBuilder:
    def __init__(self, rows_, sequence_length_, resultsDir_, fileName_):
        self._rows = rows_
        self._sequence_length = sequence_length_
        self._resultsDir = resultsDir_
        self._fileName = fileName_
        
    def build(self):
        stat_file = self._resultsDir + self._fileName
        f = open(stat_file, "w")
        for row in self._rows:
            f.write(row.name + " & ")
            if (row.follower_stat == None):
                f.write("- & ")
            else:
                follower_stat = row.follower_stat.getStatsOfSequenceLength(self._sequence_length)
                f.write("{:.4f}".format(round(follower_stat.mean, 4)) + "({:.4f}) & ".format(round(follower_stat.var, 4)))
            if (row.friends_stat == None):
                f.write("- \\")
            else:
                friends_stat = row.friends_stat.getStatsOfSequenceLength(self._sequence_length)
                f.write("{:.4f}".format(round(friends_stat.mean, 4)) + "({:.4f}) \\ ".format(round(friends_stat.var, 4)))
            f.write("\n")
        f.close()