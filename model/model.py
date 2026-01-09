import networkx as nx
from networkx.classes import neighbors

from database.dao import DAO

class Model:
    def __init__(self):
        self.teams = []
        self.G = nx.Graph()
        self.K = 3
        self.salary_map = {}
        self.team_map = {}
        self.best_path = []
        self.best_weight = 0

    def get_years(self):
        return DAO.read_year()

    def load_teams(self, year):
        self.teams = DAO.read_team_by_year(year)
        return self.teams


    def build_graph(self, year):

        self.G.clear()
        self.G.add_nodes_from(self.teams)
        self.salary_map=DAO.read_team_salary(year)

        for i,t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                w=self.salary_map.get(t1.id,0) + self.salary_map.get(t2.id,0)
                self.G.add_edge(t1,t2,weight=w)

        self.team_map = {t.id: t for t in self.teams}

    def get_neighbors(self,team):
        neighbors=[]
        for n in self.G.neighbors(team):
            w=self.G[team][n]["weight"]
            neighbors.append((n,w))
        return sorted(neighbors, key=lambda x: x[1], reverse=True)

    def calcola_percorso(self,start):

        self.best_path=[]
        self.best_weight=0
        self.ricorsione([start],0,float('inf'))
        return self.best_path, self.best_weight

    def ricorsione(self,path,weight,last_edge_weight):
        last= path[-1]
        if weight >self.best_weight:
            self.best_weight = weight
            self.best_path = path.copy()

        vicini=self.get_neighbors(last)
        neighbors=[]
        counter=0
        for node,edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_edge_weight:
                neighbors.append((node, edge_w))
                counter += 1
                if counter == self.K:
                    break
        for node, edge_w in neighbors:
            path.append(node)
            self.ricorsione(path, weight + edge_w, edge_w)
            path.pop()
