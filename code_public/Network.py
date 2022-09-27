from igraph import Graph,plot
from igraph._igraph import ADJ_DIRECTED, ADJ_UNDIRECTED

class Network:
    def __init__(self, adjacencyMx, labels, directed):
        self._adjacencyMx = adjacencyMx
        self._labels = labels
        directed_mode = ADJ_DIRECTED
        self._directed = directed
        if directed == False:
            directed_mode = ADJ_UNDIRECTED
        self._graph = Graph.Adjacency(adjacencyMx, mode = directed_mode)
        self._graph.vs["name"] = labels
        self._graph.vs["label"] = self._graph.vs["name"]
        self._id_of_label = dict()
        n = len(self._labels)
        rng = range(n)
        for index in rng:
            self._id_of_label[self._labels[index]] = index
            
         
    def plot(self, target_file):
        if len(self._adjacencyMx) > 0:
            plot(self._graph, target_file)
    #mode_ can be "in", "out" or "all"
    def neighbors(self, mode_):
        neighbors_dict = dict()
        for label in self._labels:
            neighbor_indices_of_vertex = self._graph.neighbors(label, mode = mode_)
            neighbours_set = set([self._labels[i] for i in neighbor_indices_of_vertex])
            neighbors_dict[label] = list(neighbours_set)
        return neighbors_dict
    
    def isolatedNodeIndices(self):
        n = len(self._adjacencyMx)
        rng1 = range(n)
        rng2 = range(n)
        isolatedNodes = []
        for index in rng1:
            neighbours_cnt = 0
            for i in rng2:
                if self._adjacencyMx[index][i] != 0:
                    neighbours_cnt += 1
            if self._directed:
                for i in rng2:
                    if self._adjacencyMx[i][index] != 0:
                        neighbours_cnt += 1
            if neighbours_cnt == 0:
                isolatedNodes.append(index)
                
        return isolatedNodes
    
    def isolatedNodeLabels(self):
        isolatedNodes = self.isolatedNodeIndices()
        isolatedLabels = [self._labels[i] for i in isolatedNodes]
        return  isolatedLabels
    
    def removeNodes(self, indices):
        self._graph.delete_vertices(indices)
        self._adjacencyMx = self._graph.get_adjacency()._get_data()
        labels = [self._labels[i] for i in indices]
        for label in labels:
            self._labels.remove(label)
        n = len(self._labels)
        rng = range(n)
        self._id_of_label.clear()
        for index in rng:
            self._id_of_label[self._labels[index]] = index
            
    def removeNodesWithLabel(self, labels):
        indices = []
        for label in labels:
            index = self._id_of_label.get(label)
            if index != None:
                indices.append(index)
        if len(indices) > 0:
            self.removeNodes(indices)
    
    
    def inDegree(self):
        inDegreeList = self._graph.indegree()
        inDegreeDict = dict()
        n = len(inDegreeList)
        indices = range(n)
        for index in indices:
            inDegreeDict[self._labels[index]] = inDegreeList[index]
        return inDegreeDict
    
    def neighborhood(self, steps_, mode_):
        neighbourhoodList = self._graph.neighborhood_size(order = steps_, mode = mode_)
        neighbourhoodDict = dict()
        n = len(neighbourhoodList)
        indices = range(n)
        for index in indices:
            neighbourhoodDict[self._labels[index]] = neighbourhoodList[index]
        return neighbourhoodDict
    
    def pageRank(self, damping_value):
        pagerankList = self._graph.pagerank( damping=damping_value)
        pagerankDict = dict()
        n = len(pagerankList)
        indices = range(n)
        for index in indices:
            pagerankDict[self._labels[index]] = pagerankList[index]
        return pagerankDict

    def indegPlusPageRank(self, damping_value):
        inDegreeList = self._graph.indegree()
        pagerankList = self._graph.pagerank( damping=damping_value)
        resultDict = dict()
        n = len(pagerankList)
        indices = range(n)
        for index in indices:
            resultDict[self._labels[index]] = inDegreeList[index] + pagerankList[index]
        return resultDict
    
    def labels(self):
        return self._labels
    
    def computeSymmetryRate(self):
        self._adjacencyMx = self._graph.get_adjacency()._get_data()
        symmetryCnt = 0
        edgeCnt = 0
        n = len(self._labels)
        rng = range(n)
        for i in rng:
            rng2 = range(i + 1, n)
            for j in rng2:
                s = self._adjacencyMx[i][j] + self._adjacencyMx[j][i]
                if s > 0:
                    edgeCnt = edgeCnt + 1
                if s == 2:
                    symmetryCnt = symmetryCnt + 1
        
        if edgeCnt > 0:
            ret = float(symmetryCnt) / edgeCnt
            return ret
        return 1.0
                    
    def edgeNumber(self):
        return self._graph.ecount()
    
    def closeness(self):
        closenessList = self._graph.closeness()
        closenessDict = dict()
        n = len(closenessList)
        indices = range(n)
        for index in indices:
            closenessDict[self._labels[index]] = closenessList[index]
        return closenessDict
    
    def betweenness(self, asDirected):
        closenessList = self._graph.betweenness(directed = asDirected)
        closenessDict = dict()
        n = len(closenessList)
        indices = range(n)
        for index in indices:
            closenessDict[self._labels[index]] = closenessList[index]
        return closenessDict
    
    def coreness(self, mode_):
        corenessList = self._graph.coreness(mode = mode_)
        corenessDict = dict()
        n = len(corenessList)
        indices = range(n)
        for index in indices:
            corenessDict[self._labels[index]] = corenessList[index]
        return corenessDict
    
    def eigen_centralty(self, asDirected):
        eigenList = self._graph.eigenvector_centrality(directed = asDirected)
        eigenDict = dict()
        n = len(eigenList)
        indices = range(n)
        for index in indices:
            eigenDict[self._labels[index]] = eigenList[index]
        return eigenDict