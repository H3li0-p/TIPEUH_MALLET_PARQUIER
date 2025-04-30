"""Graphes non-orienté """
class Graph :
  
    def __init__(self,nv):     
         self.nb_edges = 0
         self.mat = [[-1 for _ in range(nv)] for _ in range(nv)]
         self.nb_vertices = nv
 