import sys
from SurveyData import SurveyData
from ResultsFolderStructure import ResultsFolderStructure
from SurveyStatistics import SurveyStatistics
from FollowerData import FollowerDataReader
from SymmetryChecker import FollowerSymmetryChecker, FriendSymmetryChecker
from FriendsData import FriendsDataReader
from FollowerOpinionLeaderDataReader import FollowerOpinionLeaderDataReader
from OpinionLeaderMetrics import InDegreeMetric, PageRank65Metric, NeighborhoodInMetric, TwoHopNeighborhoodInMetric, CorenessInMetric
from OpinionLeaderMetrics import DirectedEigenMetric, ClosenessMetric, BetweennessMetric, BordaCountAggregationMetric
from FriendsOpinionLeaderDataReader import FriendsOpinionLeaderDataReader
from TemporalDataBuilder import FollowerTemporalDataBuilder, FriendsTemporalDataBuilder, AggrTemporalDataBuilder
from CounterStatistics import CounterStatisticsCalculator
from SequenceInstability import SequenceInstabilityWithJaccardCalculator
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
------------------------ build basic statistics about schools ------------------
"""
    
surveyStatistics = SurveyStatistics(resultsDir)
surveyStatistics.buildStatistics(schools)

"""
------------------------ read follower data  -----------------------
"""
     
followerDataReader = FollowerDataReader(resultsFolderStructure)
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

sequenceInstabilityOninDegree = SequenceInstabilityWithJaccardCalculator(inDegreeMetric.name())
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegree)
        
sequenceInstabilityOnPageRank65 = SequenceInstabilityWithJaccardCalculator(pageRank65Metric.name())
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65)
        
sequenceInstabilityOnTwoHopNeighborhoodIn = SequenceInstabilityWithJaccardCalculator(twoHopNeighborhoodInMetric.name())
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodIn)
    
sequenceInstabilityOncorenessIn = SequenceInstabilityWithJaccardCalculator(corenessInMetric.name())
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOncorenessIn)
    
sequenceInstabilityOnDirectedEigen = SequenceInstabilityWithJaccardCalculator(directedEigenMetric.name())
followerTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigen)

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
    
sequenceInstabilityOninDegreeOnFriends = SequenceInstabilityWithJaccardCalculator(inDegreeMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOninDegreeOnFriends)
    
sequenceInstabilityOnPageRank65OnFriends = SequenceInstabilityWithJaccardCalculator(pageRank65MetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnPageRank65OnFriends)

sequenceInstabilityOnTwoHopNeighborhoodInOnFriends = SequenceInstabilityWithJaccardCalculator(twoHopNeighborhoodInMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnTwoHopNeighborhoodInOnFriends)

sequenceInstabilityOncorenessInOnFriends = SequenceInstabilityWithJaccardCalculator(corenessInMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOncorenessInOnFriends)

sequenceInstabilityOnDirectedEigenOnFriends = SequenceInstabilityWithJaccardCalculator(directedEigenMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityOnDirectedEigenOnFriends)

sequenceInstabilityClosenessOnFriends = SequenceInstabilityWithJaccardCalculator(closenessMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityClosenessOnFriends)

sequenceInstabilityBetweennessOnFriends = SequenceInstabilityWithJaccardCalculator(betweennessMetricOnFriends.name())
friendsTemporalDataBuilder.registerCalculator(sequenceInstabilityBetweennessOnFriends)

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

sequenceInstabilityOnBordaCountAggregation = SequenceInstabilityWithJaccardCalculator(bordaCountAggregationMetricFollower.name())
followerAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregation)

followerAggrTemporalDataBuilder.read(schools)

"""
-------------------- build temporal statistics on aggregated data on followers ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregation.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation.read(schools)

"""
--------------------- compute temporal metrics on aggregated data on friends ---------------
"""

friendsAggrTemporalDataBuilder = AggrTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)

counterStatisticsCalculatorBordaCountAggregationOnFriends = CounterStatisticsCalculator(bordaCountAggregationMetricFriends.name())
friendsAggrTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBordaCountAggregationOnFriends)

sequenceInstabilityOnBordaCountAggregationOnFriends = SequenceInstabilityWithJaccardCalculator(bordaCountAggregationMetricFriends.name())
friendsAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnFriends)


friendsAggrTemporalDataBuilder.read(schools)

 
"""
-------------------- build temporal statistics on aggregated data on friends ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation_onFriends = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnFriends.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onFriends.read(schools)


"""
--------------------- compute temporal metrics on aggregated data on both followers and friends ---------------
"""

allAggrTemporalDataBuilder = AggrTemporalDataBuilder(resultsFolderStructure, resultsDir, 4)

counterStatisticsCalculatorBordaCountAggregationOnAll = CounterStatisticsCalculator(bordaCountAggregationMetricAll.name())
allAggrTemporalDataBuilder.registerCalculator(counterStatisticsCalculatorBordaCountAggregationOnAll)

sequenceInstabilityOnBordaCountAggregationOnAll = SequenceInstabilityWithJaccardCalculator(bordaCountAggregationMetricAll.name())
allAggrTemporalDataBuilder.registerCalculator(sequenceInstabilityOnBordaCountAggregationOnAll)

allAggrTemporalDataBuilder.read(schools)

"""
-------------------- build temporal statistics on aggregated data on both followers and friends ------------
"""

sequenceInstabilityStatistics_bordaCountAggregation_onAll = SequenceInstabilityStatisticsAggr(sequenceInstabilityOnBordaCountAggregationOnAll.fullName(), resultsFolderStructure, resultsDir)
sequenceInstabilityStatistics_bordaCountAggregation_onAll.read(schools)

"""
-------------------- Kendall tau correlation between the centrality measures ------------
"""

metrics_followers = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric, bordaCountAggregationMetricFollower ]
metrics_followers_names = ["iDg", "pg", "2Nbh", "core", "eign", "bca" ]

followerRankCorrelations = KendallTauCorrelation("followerKandallTau", resultsFolderStructure, resultsDir, metrics_followers, metrics_followers, metrics_followers_names, metrics_followers_names, None, None)
followerRankCorrelations.read(schools)

metrics_friends = [inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends, bordaCountAggregationMetricFriends ]
metrics_friends_names = ["iDg", "pg", "2Nbh", "core", "eign", "cl", "btw", "bca" ]

friendsRankCorrelations = KendallTauCorrelation("friendsKandallTau", resultsFolderStructure, resultsDir, metrics_friends, metrics_friends, metrics_friends_names, metrics_friends_names, None, None)
friendsRankCorrelations.read(schools)


follower_vs_friendsRankCorrelations = KendallTauCorrelation("follower_vs_friends_KandallTau", resultsFolderStructure, resultsDir, metrics_friends, metrics_followers,  metrics_friends_names, metrics_followers_names, "Advice seeking centrality measures", "Friendship centrality measures")
follower_vs_friendsRankCorrelations.read(schools)


allBordaCount_vs_followersRankCorrelations = KendallTauCorrelation("allBordaCount_vs_followers_KandallTau", resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_followers, ["bca(all)"], metrics_followers_names, "Advice seeking centrality measures", None)
allBordaCount_vs_followersRankCorrelations.read(schools)

allBordaCount_vs_friendsRankCorrelations = KendallTauCorrelation("allBordaCount_vs_friends_KandallTau", resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_friends, ["bca(all)"], metrics_friends_names, "Friendship centrality measures", None)
allBordaCount_vs_friendsRankCorrelations.read(schools)

"""
-------------------- Jaccard similarity of top influencers ------------
"""

jaccardTopInfluencersFollowers = JaccardTopInfluencersSimilarity("followerJaccard",5 ,resultsFolderStructure, resultsDir, metrics_followers, metrics_followers, metrics_followers_names, metrics_followers_names, None, None)
jaccardTopInfluencersFollowers.read(schools)

jaccardTopInfluencersFriends = JaccardTopInfluencersSimilarity("friendsJaccard",5 ,resultsFolderStructure, resultsDir, metrics_friends, metrics_friends, metrics_friends_names, metrics_friends_names, None, None)
jaccardTopInfluencersFriends.read(schools)

jaccardTopInfluencers_follower_vs_friendss = JaccardTopInfluencersSimilarity("follower_vs_friends_Jaccard",5 ,resultsFolderStructure, resultsDir, metrics_friends, metrics_followers,  metrics_friends_names, metrics_followers_names, "Advice seeking centrality measures", "Friendship centrality measures" )
jaccardTopInfluencers_follower_vs_friendss.read(schools)

jaccard_allBordaCount_vs_followers = JaccardTopInfluencersSimilarity("allBordaCount_vs_followers_Jaccard", 5, resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_followers, ["bca(all)"], metrics_followers_names, "Advice seeking centrality measures", None)
jaccard_allBordaCount_vs_followers.read(schools)

jaccard_allBordaCount_vs_friends = JaccardTopInfluencersSimilarity("allBordaCount_vs_friends_Jaccard",5, resultsFolderStructure, resultsDir, [bordaCountAggregationMetricAll], metrics_friends,["bca(all)"], metrics_friends_names, "Friendship centrality measures", None)
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

items_follower = [(FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegree.fullName(), "inDg", "#FF2709"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65.fullName(), "pg", "#09FF10"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodIn.fullName(), "2Nbh", "#FA70B5"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessIn.fullName(), "core", "#F1C40F"),
          (FOLLOWER_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigen.fullName(), "eign", "#DC7633")]

sequenceInstabilityPlotFollowers = SequenceInstabilityPlot(items_follower, "Centrality measures of advice seeking networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FollowerSequenceInstabilityPlot.png")
sequenceInstabilityPlotFollowers.read(schools)

items_friends = [(FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOninDegreeOnFriends.fullName(), "inDg", "#FF2709"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnPageRank65OnFriends.fullName(), "pg", "#09FF10"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnTwoHopNeighborhoodInOnFriends.fullName(), "2Nbh", "#FA70B5"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOncorenessInOnFriends.fullName(), "core", "#F1C40F"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityOnDirectedEigenOnFriends.fullName(), "eign", "#DC7633"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityClosenessOnFriends.fullName(), "cl", "#95A5A6"),
          (FRIEND_TEMPORAL_DATA_KEY, sequenceInstabilityBetweennessOnFriends.fullName(), "btw", "#186A3B")]


sequenceInstabilityPlotFriends= SequenceInstabilityPlot(items_friends, "Centrality measures of friendship networks", "Sequence instability",  resultsFolderStructure, resultsDir, "FriendsSequenceInstabilityPlot.png")
sequenceInstabilityPlotFriends.read(schools)

items_aggr = [(AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregation.fullName(), "advice seeking", "#FF2709"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnFriends.fullName(), "friendship", "#09FF10"),
          (AGGR_TEMPORAL_DATA_KEY, sequenceInstabilityOnBordaCountAggregationOnAll.fullName(), "both", "#0030D7")]

sequenceInstabilityPlotAggr = SequenceInstabilityPlot(items_aggr, "Borda count aggregation measures", "Sequence instability",  resultsFolderStructure, resultsDir, "AggrSequenceInstabilityPlot.png")
sequenceInstabilityPlotAggr.read(schools)

rows = list()
rows.append(SequenceInstabilityStatsTableRow("iDg",sequenceInstabilityStatisticsFollower_inDegree, sequenceInstabilityStatisticsFriends_inDegree ))
rows.append(SequenceInstabilityStatsTableRow("pg",sequenceInstabilityStatisticsFollower_PageRank65, sequenceInstabilityStatisticsFriends_PageRank65 ))
rows.append(SequenceInstabilityStatsTableRow("2Nbh",sequenceInstabilityStatisticsFollower_twoHopNeighborhoodIn, sequenceInstabilityStatisticsFriends_twoHopNeighborhoodIn ))
rows.append(SequenceInstabilityStatsTableRow("core",sequenceInstabilityStatisticsFollower_corenessIn, sequenceInstabilityStatisticsFriends_corenessIn ))
rows.append(SequenceInstabilityStatsTableRow("eign",sequenceInstabilityStatisticsFollower_directedEigen, sequenceInstabilityStatisticsFriends_directedEigen ))
rows.append(SequenceInstabilityStatsTableRow("cl",None, sequenceInstabilityStatisticsFriends_closeness ))
rows.append(SequenceInstabilityStatsTableRow("btw",None, sequenceInstabilityStatisticsFriends_betweenness ))
rows.append(SequenceInstabilityStatsTableRow("bca",sequenceInstabilityStatistics_bordaCountAggregation, sequenceInstabilityStatistics_bordaCountAggregation_onFriends )) 
 
sequenceInstabilityStatsTableBuilder_4 = SequenceInstabilityStatsTableBuilder(rows, 4, resultsDir, "sequenceInstabilityStatistics_4.txt")
sequenceInstabilityStatsTableBuilder_4.build()

sequenceInstabilityStatsTableBuilder_5 = SequenceInstabilityStatsTableBuilder(rows, 5, resultsDir, "sequenceInstabilityStatistics_5.txt")
sequenceInstabilityStatsTableBuilder_5.build()

"""
--------------------------Wave-to-wave correlations ----------------------------------------
"""

metrics_wtw = [inDegreeMetric, pageRank65Metric, twoHopNeighborhoodInMetric, corenessInMetric, directedEigenMetric, bordaCountAggregationMetricFollower,
                           inDegreeMetricOnFriends, pageRank65MetricOnFriends, twoHopNeighborhoodInMetricOnFriends, corenessInMetricOnFriends, directedEigenMetricOnFriends, closenessMetricOnFriends, betweennessMetricOnFriends, bordaCountAggregationMetricFriends,
                           bordaCountAggregationMetricAll ]
metrics_wtw_names = ["iDg-as", "pg-as", "2Nbh-as", "core-as", "eign-as", "bca-as",
                           "iDg-fr", "pg-fr", "2Nbh-fr", "core-fr", "eign-fr", "cl-fr", "btw-fr", "bca-fr",
                           "bca-all" ]

WtWCorrelations = KendallTauWaveToWaveCorrelation("KendallTau", resultsFolderStructure, resultsDir, metrics_wtw, metrics_wtw_names)
WtWCorrelations.read(schools)