import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self.solBest = 0
        self.path = []
        self.path_edge = []

    def buildGraph(self, country, year):
        all_nodes = DAO.getAllNodes(country)
        for node in all_nodes:
            self._idMap[node.Retailer_code] = node
        self._graph.add_nodes_from(all_nodes)
        allEdges = DAO.getAllEdges(country, year, self._idMap)
        self._graph.add_weighted_edges_from(allEdges)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    @staticmethod
    def getAllCountries():
        return DAO.getAllCountries()

    def getVolumiVendita(self):
        listRetailerVolume = []
        for retailer in self._graph.nodes:
            volumeVendita = 0
            neighbors = self._graph.neighbors(retailer)
            for neighbor in neighbors:
                volumeVendita += self._graph[retailer][neighbor]["weight"]
            listRetailerVolume.append((retailer, volumeVendita))
        sortedRetailerVolume = sorted(listRetailerVolume, key=lambda x: x[1], reverse=True)
        return sortedRetailerVolume

    # def getPath(self, N):
    #     self._bestPath = []
    #     self._bestScore = 0
    #     self._pathEdge = []
    #     parziale = []
    #     for node in self._graph.nodes:
    #         parziale.append(node)
    #         self._ricorsione(parziale, N, [])
    #         parziale.pop()
    #     return self._bestPath, self._bestScore
    #
    # def _ricorsione(self, parziale, N, partial_edge):
    #     last = parziale[-1]
    #     if len(partial_edge) == (N - 1):
    #         if last != parziale[0]:
    #             return
    #
    #         if self.weightSum(parziale) > self._bestScore:
    #             self._bestPath = copy.deepcopy(parziale)
    #             self._bestScore = self.weightSum
    #         return
    #
    #     vicini = self._graph.neighbors(last)
    #     for vicino in vicini:
    #         if vicino not in parziale:
    #             parziale.append(vicino)
    #             self._ricorsione(parziale, N)
    #             parziale.pop()
    #
    # def weightSum(self, mylist):
    #     somma = 0
    #     for e in mylist:
    #         somma += e[2]
    #     return somma

    def computePath(self, N):
        self.path = []
        self.path_edge = []
        self.solBest = 0

        for r in self._graph.nodes:
            partial = []
            partial.append(r)
            self.ricorsione(partial, N, [])

    def ricorsione(self, partial, N, partial_edge):
        r_last = partial[-1]
        r_first = partial[0]

        # terminazione
        if len(partial_edge) == (N - 1):
            if self._graph.has_edge(r_last, r_first):
                partial_edge.append((r_last, r_first, self._graph.get_edge_data(r_last, r_first)['weight']))
                partial.append(r_first)
                weight_path = self.computeWeightPath(partial_edge)
                if weight_path > self.solBest:
                    self.solBest = weight_path + 0.0
                    self.path = partial[:]
                    self.path_edge = partial_edge[:]
                partial.pop()
                partial_edge.pop()
            return

        neighbors = list(self._graph.neighbors(r_last))
        neighbors = [i for i in neighbors if i not in partial]
        for n in neighbors:
            partial_edge.append((r_last, n, self._graph.get_edge_data(r_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, N, partial_edge)
            partial.pop()
            partial_edge.pop()

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]
        return weight
