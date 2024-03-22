import sys
from SurveyData import SurveyData
from ResultsFolderStructure import ResultsFolderStructure
from SurveyStatistics import SurveyStatistics
from FollowerData import FollowerDataReader
from SymmetryChecker import FollowerSymmetryChecker, FriendSymmetryChecker
from FriendsData import FriendsDataReader
from FollowerOpinionLeaderDataReader import FollowerOpinionLeaderDataReader
from OpinionLeaderMetrics import InDegreeMetric, PageRank65Metric, TwoHopNeighborhoodInMetric, CorenessInMetric
from OpinionLeaderMetrics import DirectedEigenMetric, ClosenessMetric, BetweennessMetric, BordaCountAggregationMetric
from FriendsOpinionLeaderDataReader import FriendsOpinionLeaderDataReader
from TemporalDataBuilder import FollowerTemporalDataBuilder, FriendsTemporalDataBuilder, AggrTemporalDataBuilder
from CounterStatistics import CounterStatisticsCalculator
from SequenceInstability import *
from JaccardSimilarity import JaccardSimilarityCalculator
from SequenceInstabilityStatistics import SequenceInstabilityStatisticsFollower, SequenceInstabilityStatisticsFriends, SequenceInstabilityStatisticsAggr
from JaccardSimilarityStatistics import JaccardSimilarityStatisticsFollowerData, JaccardSimilarityStatisticsFrieendsData
from AggregateMetrics import AggregateMetrics
from Correlation import KendallTauCorrelation, JaccardTopInfluencersSimilarity
from CoreAnalysis import CoreAnalysis
from TemporalDataBuilder import FOLLOWER_TEMPORAL_DATA_KEY, FRIEND_TEMPORAL_DATA_KEY, AGGR_TEMPORAL_DATA_KEY
from SequenceInstabilityPlot import SequenceInstabilityPlot
from SequenceInstabilityStatsTableBuilder import *
from WaveToWaveCorrelation import KendallTauWaveToWaveCorrelation
import numpy as np
import scipy
import igraph
import seaborn as sb
import matplotlib

"""
Version informations

"""

print("Python version")
print(sys.version)
print("Version info.")
print(sys.version_info)

print("\nNumpy version:")
print(np.__version__)

print("\nScipy version:")
print(scipy.__version__)

print("\nigraph version:")
print(igraph.__version__)

print("\nseaborn version:")
print(sb.__version__)

print("\nmatplotlib version:")
print(matplotlib.__version__)


image_extensions = ".eps"

"""
-------------------------------- set paths ------------------------------------
"""
pathSep = "\\"
rootDir = "..\\"
dataDir = rootDir +  "data_public" + pathSep
resultsDir = rootDir +  "results" + pathSep

"""
-------------------------------- read surveys ----------------------------------
"""
    
surveyData = SurveyData(dataDir, pathSep, resultsDir)
schools = surveyData.read()

"""
-------- create results folder structure and the handler object ----------------
"""
    
resultsFolderStructure = ResultsFolderStructure(resultsDir, pathSep)
resultsFolderStructure.build(schools)


"""
------------------------ Sequence instability test ------------------
"""


sequenceInstabilityTester = SequenceInstabilityTopInfluencersTester(resultsFolderStructure, test_list)
sequenceInstabilityTester.run()

"""
------------------------ build basic statistics about schools ------------------
"""
    
surveyStatistics = SurveyStatistics(resultsDir)
surveyStatistics.buildStatistics(schools)

"""
------------------------ read follower data  -----------------------
"""
     
followerDataReader = FollowerDataReader(resultsFolderStructure, 4)
followerDataReader.read(schools)    

"""
------------------------ symmetry check of follower networks  -----------------------
"""
followerSymmetryChecker = FollowerSymmetryChecker(resultsFolderStructure, resultsDir)
followerSymmetryChecker.read(schools)

"""
------------------------ read friends data  -----------------------
"""
     
friendsDataReader = FriendsDataReader(resultsFolderStructure)
friendsDataReader.read(schools)

"""
------------------------ symmetry check of follower networks  -----------------------
"""

friendsSymmetryChecker = FriendSymmetryChecker(resultsFolderStructure, resultsDir)
friendsSymmetryChecker.read(schools)

"""
--------------------- find opinion leaders based on followers data  ------------
"""
      
followerOpinionLeaderDataReader = FollowerOpinionLeaderDataReader(resultsFolderStructure, resultsDir)
    
# indeg
inDegreeMetric = InDegreeMetric("follower")
followerOpinionLeaderDataReader.registerMetric(inDegreeMetric)
    
    
#pagerank 65
pageRank65Metric = PageRank65Metric("follower")
followerOpinionLeaderDataReader.registerMetric(pageRank65Metric)
        
#two hop  neighborhood
twoHopNeighborhoodInMetric = TwoHopNeighborhoodInMetric("follower")
followerOpinionLeaderDataReader.registerMetric(twoHopNeighborhoodInMetric)
    
#coreness in
corenessInMetric = CorenessInMetric("follower")
followerOpinionLeaderDataReader.registerMetric(corenessInMetric)
    
#directed eigen centrality
directedEigenMetric = DirectedEigenMetric("follower")
followerOpinionLeaderDataReader.registerMetric(directedEigenMetric)
    
    
followerOpinionLeaderDataReader.read(schools)

"""
--------------------- find opinion leaders based on friends data  ------------
"""
    
friendsOpinionLeaderDataReader = FriendsOpinionLeaderDataReader(resultsFolderStructure, resultsDir)
    
# indeg
inDegreeMetricOnFriends = InDegreeMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(inDegreeMetricOnFriends)

#pagerank
pageRank65MetricOnFriends = PageRank65Metric("friend")
friendsOpinionLeaderDataReader.registerMetric(pageRank65MetricOnFriends)

#closeness
closenessMetricOnFriends = ClosenessMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(closenessMetricOnFriends)

#betweenness
betweennessMetricOnFriends = BetweennessMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(betweennessMetricOnFriends)
        
#two hop  neighborhood
twoHopNeighborhoodInMetricOnFriends = TwoHopNeighborhoodInMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(twoHopNeighborhoodInMetricOnFriends)
    
#coreness in
corenessInMetricOnFriends = CorenessInMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(corenessInMetricOnFriends)
    
#directed eigen centrality
directedEigenMetricOnFriends = DirectedEigenMetric("friend")
friendsOpinionLeaderDataReader.registerMetric(directedEigenMetricOnFriends)
        
friendsOpinionLeaderDataReader.read(schools)

"""
--------------------- compute temporal metrics on follower data  ---------------
"""
    
followerTemporalDataBuilder = FollowerTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)


################################## COUNTER STATISTICS
      
counterStatisticsCalculatorinDegree = CounterStatisticsCalculator(inDegreeMetric.name())
followerTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorinDegree)
    
counterStatisticsCalculatorPageRank65 = CounterStatisticsCalculator(pageRank65Metric.name())
followerTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorPageRank65)
        
counterStatisticsCalculatorTwoHopNeighborhoodIn = CounterStatisticsCalculator(twoHopNeighborhoodInMetric.name())
followerTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorTwoHopNeighborhoodIn)
    
counterStatisticsCalculatorCorenessIn = CounterStatisticsCalculator(corenessInMetric.name())
followerTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorCorenessIn)
    
counterStatisticsCalculatorDirectedEigen = CounterStatisticsCalculator(directedEigenMetric.name())
followerTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorDirectedEigen)

################################## SEQUENCE INSTABILITY

sequenceInstabilityOninDegree = SequenceInstabilityTopInfluencers(inDegreeMetric.name(), 1, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegree)
        
sequenceInstabilityOnPageRank65 = SequenceInstabilityTopInfluencers(pageRank65Metric.name(), 1, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65)
        
sequenceInstabilityOnTwoHopNeighborhoodIn = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetric.name(), 1, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodIn)
    
sequenceInstabilityOncorenessIn = SequenceInstabilityTopInfluencers(corenessInMetric.name(), 1, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOncorenessIn)
    
sequenceInstabilityOnDirectedEigen = SequenceInstabilityTopInfluencers(directedEigenMetric.name(), 1, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigen)


################################## SEQUENCE INSTABILITY TOP INFLUENCERS

sequenceInstabilityOninDegree_TopK_Jaccard = SequenceInstabilityTopInfluencers(inDegreeMetric.name(), 3, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegree_TopK_Jaccard)

sequenceInstabilityOnPageRank65_TopK_Jaccard = SequenceInstabilityTopInfluencers(pageRank65Metric.name(), 5, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65_TopK_Jaccard)
        
sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_Jaccard = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetric.name(), 3, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_Jaccard)
        
sequenceInstabilityOnDirectedEigen_TopK_Jaccard = SequenceInstabilityTopInfluencers(directedEigenMetric.name(), 5, Jaccard)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigen_TopK_Jaccard)
        

sequenceInstabilityOninDegree_TopK_SFH = SequenceInstabilityTopInfluencers(inDegreeMetric.name(), 3, SFH)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegree_TopK_SFH)

sequenceInstabilityOnPageRank65_TopK_SFH = SequenceInstabilityTopInfluencers(pageRank65Metric.name(), 5, SFH)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65_TopK_SFH)
        
sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_SFH = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetric.name(), 3, SFH)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_SFH)
        
sequenceInstabilityOnDirectedEigen_TopK_SFH = SequenceInstabilityTopInfluencers(directedEigenMetric.name(), 5, SFH)
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigen_TopK_SFH)

################################## Jaccard similarity based network comparison
    
inJaccardCalculator = JaccardSimilarityCalculator(pageRank65Metric.name(),"in")
followerTemporalDataBuilder.registerCalculator(inJaccardCalculator)
    
followerTemporalDataBuilder.read(schools)

"""
-------------------- build temporal statistics on follower data ------------
"""

    
################################## SEQUENCE INSTABILITY

sequenceInstabilityStatisticsFollower_inDegree = SequenceInstabilityStatisticsFollower(sequenceInstabilityOninDegree.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_inDegree.read(schools)

sequenceInstabilityStatisticsFollower_PageRank65 = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnPageRank65.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_PageRank65.read(schools)


sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnTwoHopNeighborhoodIn.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn.read(schools)

sequenceInstabilityStatisticsFollower_corenessIn = SequenceInstabilityStatisticsFollower(sequenceInstabilityOncorenessIn.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_corenessIn.read(schools)

sequenceInstabilityStatisticsFollower_directedEigen = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnDirectedEigen.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_directedEigen.read(schools)


################################## SEQUENCE INSTABILITY OF TOP INFLUENCERS

sequenceInstabilityStatisticsFollower_inDegree_TopK_Jaccard = SequenceInstabilityStatisticsFollower(sequenceInstabilityOninDegree_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_inDegree_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFollower_PageRank65_TopK_Jaccard = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnPageRank65_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_PageRank65_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_Jaccard = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFollower_directedEigen_TopK_Jaccard = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnDirectedEigen_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_directedEigen_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFollower_inDegree_TopK_SFH = SequenceInstabilityStatisticsFollower(sequenceInstabilityOninDegree_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_inDegree_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFollower_PageRank65_TopK_SFH = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnPageRank65_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_PageRank65_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_SFH = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFollower_directedEigen_TopK_SFH = SequenceInstabilityStatisticsFollower(sequenceInstabilityOnDirectedEigen_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFollower_directedEigen_TopK_SFH.read(schools)


 

################################## Jaccard similarity based network comparison
    
inDegJaccardSimilarityStatisticsFollowerData = JaccardSimilarityStatisticsFollowerData(inJaccardCalculator.fullName(),resultsFolderStructure, resultsDir)
inDegJaccardSimilarityStatisticsFollowerData.read(schools)


"""
--------------------- compute temporal metrics on friends data  ---------------
"""

friendsTemporalDataBuilder = FriendsTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)
  
  
################################## COUNTER STATISTICS
  
counterStatisticsCalculatorinDegreeOnFriends = CounterStatisticsCalculator(inDegreeMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorinDegreeOnFriends)

counterStatisticsCalculatorPageRank65OnFriends = CounterStatisticsCalculator(pageRank65MetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorPageRank65OnFriends)

counterStatisticsCalculatorTwoHopNeighborhoodInOnFriends = CounterStatisticsCalculator(twoHopNeighborhoodInMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorTwoHopNeighborhoodInOnFriends)

counterStatisticsCalculatorCorenessInOnFriends = CounterStatisticsCalculator(corenessInMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorCorenessInOnFriends)

counterStatisticsCalculatorDirectedEigenOnFriends = CounterStatisticsCalculator(directedEigenMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorDirectedEigenOnFriends)

counterStatisticsCalculatorClosenessOnFriends = CounterStatisticsCalculator(closenessMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorClosenessOnFriends)

counterStatisticsCalculatorBetweennessOnFriends = CounterStatisticsCalculator(betweennessMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBetweennessOnFriends)

################################## SEQUENCE INSTABILITY
    
sequenceInstabilityOninDegreeOnFriends = SequenceInstabilityTopInfluencers(inDegreeMetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegreeOnFriends)
    
sequenceInstabilityOnPageRank65OnFriends = SequenceInstabilityTopInfluencers(pageRank65MetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65OnFriends)

sequenceInstabilityOnTwoHopNeighborhoodInOnFriends = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetricOnFriends.name(), 1,Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends)

sequenceInstabilityOncorenessInOnFriends = SequenceInstabilityTopInfluencers(corenessInMetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOncorenessInOnFriends)

sequenceInstabilityOnDirectedEigenOnFriends = SequenceInstabilityTopInfluencers(directedEigenMetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigenOnFriends)

sequenceInstabilityClosenessOnFriends = SequenceInstabilityTopInfluencers(closenessMetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityClosenessOnFriends)

sequenceInstabilityBetweennessOnFriends = SequenceInstabilityTopInfluencers(betweennessMetricOnFriends.name(), 1, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityBetweennessOnFriends)

################################## SEQUENCE INSTABILITY OF TOP INFLUENCERS


sequenceInstabilityOninDegreeOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(inDegreeMetricOnFriends.name(), 3, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegreeOnFriends_TopK_Jaccard)
    
sequenceInstabilityOnPageRank65OnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(pageRank65MetricOnFriends.name(), 5, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65OnFriends_TopK_Jaccard)

sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetricOnFriends.name(), 3, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_Jaccard)

sequenceInstabilityOnDirectedEigenOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(directedEigenMetricOnFriends.name(), 5, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigenOnFriends_TopK_Jaccard)

sequenceInstabilityClosenessOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(closenessMetricOnFriends.name(), 5, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityClosenessOnFriends_TopK_Jaccard)

sequenceInstabilityBetweennessOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(betweennessMetricOnFriends.name(), 5, Jaccard)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityBetweennessOnFriends_TopK_Jaccard)

sequenceInstabilityOninDegreeOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(inDegreeMetricOnFriends.name(), 3, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegreeOnFriends_TopK_SFH)
    
sequenceInstabilityOnPageRank65OnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(pageRank65MetricOnFriends.name(), 5, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65OnFriends_TopK_SFH)

sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(twoHopNeighborhoodInMetricOnFriends.name(), 3, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_SFH)

sequenceInstabilityOnDirectedEigenOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(directedEigenMetricOnFriends.name(), 5, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigenOnFriends_TopK_SFH)

sequenceInstabilityClosenessOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(closenessMetricOnFriends.name(), 5, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityClosenessOnFriends_TopK_SFH)

sequenceInstabilityBetweennessOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(betweennessMetricOnFriends.name(), 5, SFH)
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityBetweennessOnFriends_TopK_SFH)

################################## Jaccard similarity based network comparison
    
inJaccardCalculatorOnFriends = JaccardSimilarityCalculator(pageRank65MetricOnFriends.name(),"in")
friendsTemporalDataBuilder.registerCalculator(inJaccardCalculatorOnFriends)

friendsTemporalDataBuilder.read(schools)


"""
-------------------- build temporal statistics on friends data ------------
"""


################################## SEQUENCE INSTABILITY

sequenceInstabilityStatisticsFriends_inDegree = SequenceInstabilityStatisticsFriends(sequenceInstabilityOninDegreeOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_inDegree.read(schools)

sequenceInstabilityStatisticsFriends_PageRank65 = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnPageRank65OnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_PageRank65.read(schools)

sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn.read(schools)

sequenceInstabilityStatisticsFriends_corenessIn = SequenceInstabilityStatisticsFriends(sequenceInstabilityOncorenessInOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_corenessIn.read(schools)

sequenceInstabilityStatisticsFriends_directedEigen = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnDirectedEigenOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_directedEigen.read(schools)

sequenceInstabilityStatisticsFriends_closeness = SequenceInstabilityStatisticsFriends(sequenceInstabilityClosenessOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_closeness.read(schools)

sequenceInstabilityStatisticsFriends_betweenness = SequenceInstabilityStatisticsFriends(sequenceInstabilityBetweennessOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_betweenness.read(schools)

################################## SEQUENCE INSTABILITY OF TOP INFLUENCERS

sequenceInstabilityStatisticsFriends_inDegree_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityOninDegreeOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_inDegree_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFriends_PageRank65_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnPageRank65OnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_PageRank65_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFriends_directedEigen_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnDirectedEigenOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_directedEigen_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFriends_closeness_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityClosenessOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_closeness_TopK_Jaccard.read(schools)

sequenceInstabilityStatisticsFriends_betweenness_TopK_Jaccard = SequenceInstabilityStatisticsFriends(sequenceInstabilityBetweennessOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_betweenness_TopK_Jaccard.read(schools)


sequenceInstabilityStatisticsFriends_inDegree_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityOninDegreeOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_inDegree_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFriends_PageRank65_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnPageRank65OnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_PageRank65_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFriends_directedEigen_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityOnDirectedEigenOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_directedEigen_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFriends_closeness_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityClosenessOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_closeness_TopK_SFH.read(schools)

sequenceInstabilityStatisticsFriends_betweenness_TopK_SFH = SequenceInstabilityStatisticsFriends(sequenceInstabilityBetweennessOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatisticsFriends_betweenness_TopK_SFH.read(schools)

################################## Jaccard similarity based network compare
     

inDegJaccardSimilarityStatisticsFriendsData = JaccardSimilarityStatisticsFrieendsData(inJaccardCalculatorOnFriends.fullName(),resultsFolderStructure, resultsDir)
inDegJaccardSimilarityStatisticsFriendsData.read(schools)
   
"""
------------------------------------------- aggregation ---------------
"""



aggregateMetrics = AggregateMetrics(resultsFolderStructure, resultsDir)
aggr_metrics_followers = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric ]
bordaCountAggregationMetricFollower = BordaCountAggregationMetric("FollowerBordaCountAggr", 0.3, 0.7, aggr_metrics_followers)
aggregateMetrics.registerMetric(bordaCountAggregationMetricFollower)

aggr_metrics_friends = [inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends ]
bordaCountAggregationMetricFriends = BordaCountAggregationMetric("FriendsBordaCountAggr", 0.3, 0.7, aggr_metrics_friends)
aggregateMetrics.registerMetric(bordaCountAggregationMetricFriends)

aggr_metrics_all = aggr_metrics_followers + aggr_metrics_friends;
bordaCountAggregationMetricAll = BordaCountAggregationMetric("AllBordaCountAggr", 0.3, 0.7, aggr_metrics_all)
aggregateMetrics.registerMetric(bordaCountAggregationMetricAll)

aggregateMetrics.read(schools)

"""
--------------------- compute temporal metrics on aggregated data on followers---------------
"""

followerAggrTemporalDataBuilder = AggrTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)

counterStatisticsCalculatorBordaCountAggregation = CounterStatisticsCalculator(bordaCountAggregationMetricFollower.name())
followerAggrTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBordaCountAggregation)

sequenceInstabilityOnBordaCountAggregation = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFollower.name(), 1, Jaccard)
followerAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregation)

sequenceInstabilityOnBordaCountAggregation_TopK_Jaccard = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFollower.name(), 5, Jaccard)
followerAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregation_TopK_Jaccard)

sequenceInstabilityOnBordaCountAggregation_TopK_SFH = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFollower.name(), 5, SFH)
followerAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregation_TopK_SFH)

followerAggrTemporalDataBuilder.read(schools)

"""
-------------------- build temporal statistics on aggregated data on followers ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregation.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_TopK_Jaccard = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregation_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_TopK_Jaccard.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_TopK_SFH = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregation_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_TopK_SFH.read(schools)

"""
--------------------- compute temporal metrics on aggregated data on friends ---------------
"""

friendsAggrTemporalDataBuilder = AggrTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)

counterStatisticsCalculatorBordaCountAggregationOnFriends = CounterStatisticsCalculator(bordaCountAggregationMetricFriends.name())
friendsAggrTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBordaCountAggregationOnFriends)

sequenceInstabilityOnBordaCountAggregationOnFriends = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFriends.name(), 1, Jaccard)
friendsAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnFriends)

sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_Jaccard = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFriends.name(), 5, Jaccard)
friendsAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_Jaccard)

sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_SFH = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricFriends.name(), 5, SFH)
friendsAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_SFH)


friendsAggrTemporalDataBuilder.read(schools)

 
"""
-------------------- build temporal statistics on aggregated data on friends ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation_onFriends = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onFriends.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_Jaccard = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_Jaccard.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_SFH = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_SFH.read(schools)

"""
--------------------- compute temporal metrics on aggregated data on both followers and friends ---------------
"""

allAggrTemporalDataBuilder = AggrTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)

counterStatisticsCalculatorBordaCountAggregationOnAll = CounterStatisticsCalculator(bordaCountAggregationMetricAll.name())
allAggrTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBordaCountAggregationOnAll)

sequenceInstabilityOnBordaCountAggregationOnAll = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricAll.name(), 1, Jaccard)
allAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnAll)

sequenceInstabilityOnBordaCountAggregationOnAll_TopK_Jaccard = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricAll.name(), 5, Jaccard)
allAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnAll_TopK_Jaccard)

sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH = SequenceInstabilityTopInfluencers(bordaCountAggregationMetricAll.name(), 5, SFH)
allAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH)


allAggrTemporalDataBuilder.read(schools)

"""
-------------------- build temporal statistics on aggregated data on both followers and friends ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation_onAll = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnAll.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onAll.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_onAll_TopK_Jaccard = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnAll_TopK_Jaccard.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onAll_TopK_Jaccard.read(schools)

sequenceInstabilityStatistics_bordaCountAggregation_onAll_TopK_SFH = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onAll_TopK_SFH.read(schools)


"""
-------------------- Kendall tau correlation between the centrality measures ------------
"""

metrics_followers = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric, bordaCountAggregationMetricFollower ]
metrics_followers_names = ["iDg", "pg", "2Nbh", "core", "eign", "Bca" ]

followerRankCorrelations = KendallTauCorrelation("followerKandallTau", resultsFolderStructure, resultsDir, metrics_followers, metrics_followers, metrics_followers_names, metrics_followers_names, None, None, False)
followerRankCorrelations.read(schools)

metrics_friends = [inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends, bordaCountAggregationMetricFriends ]
metrics_friends_names = ["iDg", "pg", "2Nbh", "core", "eign", "cl", "btw", "Bca" ]

friendsRankCorrelations = KendallTauCorrelation("friendsKandallTau", resultsFolderStructure, resultsDir, metrics_friends, metrics_friends, metrics_friends_names, metrics_friends_names, None, None, False)
friendsRankCorrelations.read(schools)


follower_vs_friendsRankCorrelations = KendallTauCorrelation("follower_vs_friends_KandallTau", resultsFolderStructure, resultsDir, metrics_friends, metrics_followers,  metrics_friends_names, metrics_followers_names, "Advice seeking centrality measures", "Friendship centrality measures", True)
follower_vs_friendsRankCorrelations.read(schools)


allBordaCount_vs_followersRankCorrelations = KendallTauCorrelation("allBordaCount_vs_followers_KandallTau", resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_followers, ["Bca(all)"], metrics_followers_names, "Advice seeking centrality measures", None, False)
allBordaCount_vs_followersRankCorrelations.read(schools)

allBordaCount_vs_friendsRankCorrelations = KendallTauCorrelation("allBordaCount_vs_friends_KandallTau", resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_friends, ["Bca(all)"], metrics_friends_names, "Friendship centrality measures", None, False)
allBordaCount_vs_friendsRankCorrelations.read(schools)

"""
-------------------- Jaccard similarity of top influencers ------------
"""

jaccardTopInfluencersFollowers = JaccardTopInfluencersSimilarity("followerJaccard",5 ,resultsFolderStructure, resultsDir, metrics_followers, metrics_followers, metrics_followers_names, metrics_followers_names, None, None, False, image_extensions)
jaccardTopInfluencersFollowers.read(schools)

jaccardTopInfluencersFriends = JaccardTopInfluencersSimilarity("friendsJaccard",5 ,resultsFolderStructure, resultsDir, metrics_friends, metrics_friends, metrics_friends_names, metrics_friends_names, None, None, False, image_extensions)
jaccardTopInfluencersFriends.read(schools)

jaccardTopInfluencers_follower_vs_friendss = JaccardTopInfluencersSimilarity("follower_vs_friends_Jaccard",5 ,resultsFolderStructure, resultsDir, metrics_friends, metrics_followers,  metrics_friends_names, metrics_followers_names, "Advice seeking centrality measures", "Friendship centrality measures", True, image_extensions )
jaccardTopInfluencers_follower_vs_friendss.read(schools)

jaccard_allBordaCount_vs_followers = JaccardTopInfluencersSimilarity("allBordaCount_vs_followers_Jaccard", 5, resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_followers, ["Bca(all)"], metrics_followers_names, "Advice seeking centrality measures", None, False, image_extensions)
jaccard_allBordaCount_vs_followers.read(schools)

jaccard_allBordaCount_vs_friends = JaccardTopInfluencersSimilarity("allBordaCount_vs_friends_Jaccard",5, resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_friends,["Bca(all)"], metrics_friends_names, "Friendship centrality measures", None, False, image_extensions)
jaccard_allBordaCount_vs_friends.read(schools)


"""
-------------------------- Core analysis ----------------------------------------
"""

metric_to_core_analysis = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric, bordaCountAggregationMetricFollower,
                           inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends, bordaCountAggregationMetricFriends,
                           bordaCountAggregationMetricAll ]

coreAnalysisFollowers = CoreAnalysis(corenessInMetric.unique_name(), metric_to_core_analysis, resultsFolderStructure, resultsDir)
coreAnalysisFollowers.read(schools)

coreAnalysisFriends = CoreAnalysis(corenessInMetricOnFriends.unique_name(), metric_to_core_analysis, resultsFolderStructure, resultsDir)
coreAnalysisFriends.read(schools)

"""
-------------------------- Create plots and tables ----------------------------------------
"""

# FOLLOWERS

items_follower = [(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree.fullName(), "inDg", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65.fullName(), "pg", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn.fullName(), "2Nbh", "#FA70B5"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessIn.fullName(), "core", "#F1C40F"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen.fullName(), "eign", "#DC7633")]

sequenceInstabilityPlotFollowers = SequenceInstabilityPlot(items_follower, "Centrality measures of advice seeking networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot" + image_extensions)
sequenceInstabilityPlotFollowers.read(schools)

items_follower_topK_Jaccard = [(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree_TopK_Jaccard.fullName(), "inDg-3", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65_TopK_Jaccard.fullName(), "pg-5", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_Jaccard.fullName(), "2Nbh-3", "#FA70B5"),
          #(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessIn.fullName(), "core-1", "#F1C40F"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen_TopK_Jaccard.fullName(), "eign-5", "#DC7633")]

sequenceInstabilityPlotFollowers_topK_Jaccard = SequenceInstabilityPlot(items_follower_topK_Jaccard, "Centrality measures of advice seeking networks", "Top-k Sequence instability using Jaccard-distance",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot_topK_Jaccard"+ image_extensions)
sequenceInstabilityPlotFollowers_topK_Jaccard.read(schools)

items_follower_topK_SFH = [(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree_TopK_SFH.fullName(), "inDg-3", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65_TopK_SFH.fullName(), "pg-5", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_SFH.fullName(), "2Nbh-3", "#FA70B5"),
          #(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessIn.fullName(), "core-1", "#F1C40F"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen_TopK_SFH.fullName(), "eign-5", "#DC7633")]

sequenceInstabilityPlotFollowers_topK_SFH = SequenceInstabilityPlot(items_follower_topK_SFH, "Centrality measures of advice seeking networks", "Top-k Sequence instability using SFH-distance",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot_topK_SFH" + image_extensions)
sequenceInstabilityPlotFollowers_topK_SFH.read(schools)



items_follower_2Nbh_pg_core = [
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn.fullName(), "2Nbh-J-1", "#FA70B5"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_Jaccard.fullName(), "2Nbh-J-3", "#FA70B5"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn_TopK_SFH.fullName(), "2Nbh-S-3", "#FA70B5"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65.fullName(), "pg-J-1", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65_TopK_Jaccard.fullName(), "pg-J-5", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65_TopK_SFH.fullName(), "pg-S-5", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessIn.fullName(), "core-J-1", "#F1C40F"),
         ]

sequenceInstabilityPlotFollowers_2Nbh_pg_core = SequenceInstabilityPlot(items_follower_2Nbh_pg_core, "Centrality measures of advice seeking networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot_2Nbh_pg_core" + image_extensions)
sequenceInstabilityPlotFollowers_2Nbh_pg_core.read(schools)

items_follower_iDg_eign = [
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree.fullName(), "inDg-J-1", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree_TopK_Jaccard.fullName(), "inDg-J-3", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree_TopK_SFH.fullName(), "inDg-S-3", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen.fullName(), "eign-J-1", "#DC7633"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen_TopK_Jaccard.fullName(), "eign-J-5", "#DC7633"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen_TopK_SFH.fullName(), "eign-S-5", "#DC7633")
         ]

sequenceInstabilityPlotFollowers_iDg_eign = SequenceInstabilityPlot(items_follower_iDg_eign, "Centrality measures of advice seeking networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot_iDg_eign" + image_extensions)
sequenceInstabilityPlotFollowers_iDg_eign.read(schools)

# FRIENDS
items_friends = [(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends.fullName(), "inDg", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends.fullName(), "pg", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends.fullName(), "2Nbh", "#FA70B5"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessInOnFriends.fullName(), "core", "#F1C40F"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends.fullName(), "eign", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends.fullName(), "cl", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends.fullName(), "btw", "#186A3B")]


sequenceInstabilityPlotFriends= SequenceInstabilityPlot(items_friends, "Centrality measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot"+ image_extensions)
sequenceInstabilityPlotFriends.read(schools)

items_friends_TopK_Jaccard = [(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends_TopK_Jaccard.fullName(), "inDg-3", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends_TopK_Jaccard.fullName(), "pg-5", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_Jaccard.fullName(), "2Nbh-3", "#FA70B5"),
          #(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessInOnFriends.fullName(), "core-1", "#F1C40F"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends_TopK_Jaccard.fullName(), "eign-5", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends_TopK_Jaccard.fullName(), "cl-5", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends_TopK_Jaccard.fullName(), "btw-5", "#186A3B")]


sequenceInstabilityPlotFriends_TopK_Jaccard = SequenceInstabilityPlot(items_friends_TopK_Jaccard, "Centrality measures of friendship networks", "Top-k Sequence instability using Jaccard-distance",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot_topK_Jaccard" + image_extensions)
sequenceInstabilityPlotFriends_TopK_Jaccard.read(schools)

items_friends_TopK_SFH = [(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends_TopK_SFH.fullName(), "inDg-3", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends_TopK_SFH.fullName(), "pg-5", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_SFH.fullName(), "2Nbh-3", "#FA70B5"),
          #(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessInOnFriends.fullName(), "core-1", "#F1C40F"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends_TopK_SFH.fullName(), "eign-5", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends_TopK_SFH.fullName(), "cl-5", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends_TopK_SFH.fullName(), "btw-5", "#186A3B")]


sequenceInstabilityPlotFriends_TopK_SFH = SequenceInstabilityPlot(items_friends_TopK_SFH, "Centrality measures of friendship networks", "Top-k Sequence instability using SFH-distance",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot_topK_SFH" + image_extensions)
sequenceInstabilityPlotFriends_TopK_SFH.read(schools)

items_friends_2Nbh_pg_core = [
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends.fullName(), "2Nbh-J-1", "#FA70B5"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_Jaccard.fullName(), "2Nbh-J-3", "#FA70B5"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends_TopK_SFH.fullName(), "2Nbh-S-3", "#FA70B5"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends.fullName(), "pg-J-1", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends_TopK_Jaccard.fullName(), "pg-J-5", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends_TopK_SFH.fullName(), "pg-S-5", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessInOnFriends.fullName(), "core-J-1", "#F1C40F")
          ]


sequenceInstabilityPlotFriends_2Nbh_pg_core = SequenceInstabilityPlot(items_friends_2Nbh_pg_core, "Centrality measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot_2Nbh_pg_core" + image_extensions)
sequenceInstabilityPlotFriends_2Nbh_pg_core.read(schools)

items_friends_inDg_eign = [
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends.fullName(), "inDg-J-1", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends_TopK_Jaccard.fullName(), "inDg-J-3", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends_TopK_SFH.fullName(), "inDg-S-3", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends.fullName(), "eign-J-1", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends_TopK_Jaccard.fullName(), "eign-J-5", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends_TopK_SFH.fullName(), "eign-S-5", "#DC7633")
          ]


sequenceInstabilityPlotFriends_inDg_eign = SequenceInstabilityPlot(items_friends_inDg_eign, "Centrality measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot_inDg_eign" + image_extensions)
sequenceInstabilityPlotFriends_inDg_eign.read(schools)

items_friends_cl_btw = [
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends.fullName(), "cl-J-1", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends_TopK_Jaccard.fullName(), "cl-J-5", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends_TopK_SFH.fullName(), "cl-S-5", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends.fullName(), "btw-J-1", "#186A3B"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends_TopK_Jaccard.fullName(), "btw-J-5", "#186A3B"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends_TopK_SFH.fullName(), "btw-S-5", "#186A3B")
          ]


sequenceInstabilityPlotFriends_cl_btw = SequenceInstabilityPlot(items_friends_cl_btw, "Centrality measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot_cl_btw" + image_extensions)
sequenceInstabilityPlotFriends_cl_btw.read(schools)

items_aggr = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation.fullName(), "advice seeking", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends.fullName(), "friendship", "#09FF10"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll.fullName(), "both", "#0030D7")]

sequenceInstabilityPlotAggr = SequenceInstabilityPlot(items_aggr, "Borda count aggregation measures", "Sequence instability",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot" + image_extensions)
sequenceInstabilityPlotAggr.read(schools)

items_aggr_TopK_Jaccard = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation_TopK_Jaccard.fullName(), "advice seeking-5", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_Jaccard.fullName(), "friendship-5", "#09FF10"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll_TopK_Jaccard.fullName(), "both-5", "#0030D7")]

sequenceInstabilityPlotAggr_TopK_Jaccard = SequenceInstabilityPlot(items_aggr_TopK_Jaccard, "Borda count aggregation measures", "Top-k Sequence instability using Jaccard-distance",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot_topK_Jaccard" + image_extensions)
sequenceInstabilityPlotAggr_TopK_Jaccard.read(schools)

items_aggr_TopK_SFH = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation_TopK_SFH.fullName(), "advice seeking-5", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_SFH.fullName(), "friendship-5", "#09FF10"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH.fullName(), "both-5", "#0030D7")]

sequenceInstabilityPlotAggr_TopK_SFH = SequenceInstabilityPlot(items_aggr_TopK_SFH, "Borda count aggregation measures", "Top-k Sequence instability using SFH-distance",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot_topK_SFH" + image_extensions)
sequenceInstabilityPlotAggr_TopK_SFH.read(schools)

items_aggr_followers = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation.fullName(), "Bca", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation_TopK_Jaccard.fullName(), "Bca-J-5", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation_TopK_SFH.fullName(), "Bca-S-5", "#FF2709")]

sequenceInstabilityPlotAggr_followers = SequenceInstabilityPlot(items_aggr_followers, "Borda count aggregation measures of advice seeking networks", "Sequence instability",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot_followers" + image_extensions)
sequenceInstabilityPlotAggr_followers.read(schools)


items_aggr_friends = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends.fullName(), "Bca", "#09FF10"),
           (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends_TopK_Jaccard.fullName(), "Bca-J-5", "#09FF10"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH.fullName(), "Bca-S-5", "#09FF10")]

sequenceInstabilityPlotAggr_friends = SequenceInstabilityPlot(items_aggr_friends, "Borda count aggregation measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot_friends" + image_extensions)
sequenceInstabilityPlotAggr_friends.read(schools)

items_aggr_all = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll.fullName(), "Bca", "#0030D7"),
           (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll_TopK_Jaccard.fullName(), "Bca-J-5", "#0030D7"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll_TopK_SFH.fullName(), "Bca-S-5", "#0030D7")]

sequenceInstabilityPlotAggr_all = SequenceInstabilityPlot(items_aggr_all, "Borda count aggregation measures of both network types", "Sequence instability",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot_all" + image_extensions)
sequenceInstabilityPlotAggr_all.read(schools)


rows = list()
rows.append(SequenceInstabilityStatsTableRow("iDg",sequenceInstabilityStatisticsFollower_inDegree, sequenceInstabilityStatisticsFriends_inDegree ))
rows.append(SequenceInstabilityStatsTableRow("pg",sequenceInstabilityStatisticsFollower_PageRank65, sequenceInstabilityStatisticsFriends_PageRank65 ))
rows.append(SequenceInstabilityStatsTableRow("2Nbh",sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn, sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn ))
rows.append(SequenceInstabilityStatsTableRow("core",sequenceInstabilityStatisticsFollower_corenessIn, sequenceInstabilityStatisticsFriends_corenessIn ))
rows.append(SequenceInstabilityStatsTableRow("eign",sequenceInstabilityStatisticsFollower_directedEigen, sequenceInstabilityStatisticsFriends_directedEigen ))
rows.append(SequenceInstabilityStatsTableRow("cl",None, sequenceInstabilityStatisticsFriends_closeness ))
rows.append(SequenceInstabilityStatsTableRow("btw",None, sequenceInstabilityStatisticsFriends_betweenness ))
rows.append(SequenceInstabilityStatsTableRow("Bca",sequenceInstabilityStatistics_bordaCountAggregation, sequenceInstabilityStatistics_bordaCountAggregation_onFriends )) 
 
sequenceInstabilityStatsTableBuilder_4 = SequenceInstabilityStatsTableBuilder(rows, 4, resultsDir, "sequenceInstabilityStatistics_4.txt")
sequenceInstabilityStatsTableBuilder_4.build()

sequenceInstabilityStatsTableBuilder_5 = SequenceInstabilityStatsTableBuilder(rows, 5, resultsDir, "sequenceInstabilityStatistics_5.txt")
sequenceInstabilityStatsTableBuilder_5.build()

rows_TopK_Jaccard = list()
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("iDg-3",sequenceInstabilityStatisticsFollower_inDegree_TopK_Jaccard, sequenceInstabilityStatisticsFriends_inDegree_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("pg-5",sequenceInstabilityStatisticsFollower_PageRank65_TopK_Jaccard, sequenceInstabilityStatisticsFriends_PageRank65_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("2Nbh-3",sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_Jaccard, sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("core-1",sequenceInstabilityStatisticsFollower_corenessIn, sequenceInstabilityStatisticsFriends_corenessIn ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("eign-5",sequenceInstabilityStatisticsFollower_directedEigen_TopK_Jaccard, sequenceInstabilityStatisticsFriends_directedEigen_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("cl-5",None, sequenceInstabilityStatisticsFriends_closeness_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("btw-5",None, sequenceInstabilityStatisticsFriends_betweenness_TopK_Jaccard ))
rows_TopK_Jaccard.append(SequenceInstabilityStatsTableRow("Bca-5",sequenceInstabilityStatistics_bordaCountAggregation_TopK_Jaccard, sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_Jaccard )) 
 
sequenceInstabilityStatsTableBuilder_TopK_4_Jaccard = SequenceInstabilityStatsTableBuilder(rows_TopK_Jaccard, 4, resultsDir, "sequenceInstabilityStatistics_TopK_Jaccard_4.txt")
sequenceInstabilityStatsTableBuilder_TopK_4_Jaccard.build()

sequenceInstabilityStatsTableBuilder_TopK_5_Jaccard = SequenceInstabilityStatsTableBuilder(rows_TopK_Jaccard, 5, resultsDir, "sequenceInstabilityStatistics_TopK_Jaccard_5.txt")
sequenceInstabilityStatsTableBuilder_TopK_5_Jaccard.build()

rows_TopK_SFH = list()
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("iDg-3",sequenceInstabilityStatisticsFollower_inDegree_TopK_SFH, sequenceInstabilityStatisticsFriends_inDegree_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("pg-5",sequenceInstabilityStatisticsFollower_PageRank65_TopK_SFH, sequenceInstabilityStatisticsFriends_PageRank65_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("2Nbh-3",sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn_TopK_SFH, sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("core-1",sequenceInstabilityStatisticsFollower_corenessIn, sequenceInstabilityStatisticsFriends_corenessIn ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("eign-5",sequenceInstabilityStatisticsFollower_directedEigen_TopK_SFH, sequenceInstabilityStatisticsFriends_directedEigen_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("cl-5",None, sequenceInstabilityStatisticsFriends_closeness_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("btw-5",None, sequenceInstabilityStatisticsFriends_betweenness_TopK_SFH ))
rows_TopK_SFH.append(SequenceInstabilityStatsTableRow("Bca-5",sequenceInstabilityStatistics_bordaCountAggregation_TopK_SFH, sequenceInstabilityStatistics_bordaCountAggregation_onFriends_TopK_SFH )) 
 
sequenceInstabilityStatsTableBuilder_TopK_4_SFH = SequenceInstabilityStatsTableBuilder(rows_TopK_SFH, 4, resultsDir, "sequenceInstabilityStatistics_TopK_SFH_4.txt")
sequenceInstabilityStatsTableBuilder_TopK_4_SFH.build()

sequenceInstabilityStatsTableBuilder_TopK_5_SFH = SequenceInstabilityStatsTableBuilder(rows_TopK_SFH, 5, resultsDir, "sequenceInstabilityStatistics_TopK_SFH_5.txt")
sequenceInstabilityStatsTableBuilder_TopK_5_SFH.build()

"""
--------------------------Wave-to-wave correlations ----------------------------------------
"""

metrics_wtw = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric, bordaCountAggregationMetricFollower,
                           inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends, bordaCountAggregationMetricFriends,
                           bordaCountAggregationMetricAll ]
metrics_wtw_names = ["iDg-as", "pg-as", "2Nbh-as", "core-as", "eign-as", "Bca-as",
                           "iDg-fr", "pg-fr", "2Nbh-fr", "core-fr", "eign-fr", "cl-fr", "btw-fr", "Bca-fr",
                           "Bca-all" ]

WtWCorrelations = KendallTauWaveToWaveCorrelation("KendallTau", resultsFolderStructure, resultsDir, metrics_wtw, metrics_wtw_names)
WtWCorrelations.read(schools)