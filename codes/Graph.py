"""Graphes non-orienté """
class Graph :
  
    def __init__(self,nv):     
         self.nb_edges = 0
         self.mat = [[-1 for _ in range(nv)] for _ in range(nv)]
         self.nb_vertices = nv
 
    def get_adj_tab(self):
        """Renvoie une liste d'adjacence associant à chaque sommet ses voisins directs, par ordre croissant de distance les séparants"""
        nv = self.nb_vertices - 1 #Les nv sommets sont étiquetés de 0 à nv-1
        mat_adj = self.mat
        tab_adj = [[] for _ in range(nv)] #tableau contenant nv listes, la i-eme liste contenant les voisins du i-eme sommet
            for sommet in range(nv):
                for voisin in range(nv):
                    if ( mat_adj[sommet][voisin]!= -1):
                        tab_adj[sommet].append(voisin) # on ajoute le voisin à la liste si il est bien voisin direct du sommet étudié
        return tab_adj.sorted()

"""Note : la fonction get_adj_tab a un coût élevé (améliorable ?), mais permet par la suite d'accéder aux plus proches voisins de chaque sommet en temps cst
"""

    def get_lin_mat(self):
        """Donne la version linéarisée de la matrice d'adjacence du graphe : celui-ci étant non-orienté, sa matrice d'adjacence est symétrique"""
        nv = self.nb_vertices - 1 #-1 pour pouvoir itérer (les nv sommets sont étiquetés de 0 à n-1
        mat_adj = self.mat
        lin_adj = []
        for i in range(nv):
            for j in range(i+1,nv):
                lin_adj.append(mat_adj[i][j])
        return lin_adj

                            """[ [-1, 3, 4, 7,-1, 1], exemple de matrice complète, la linéarisation donnerait: 
                                 [ 3,-1, 5, 3, 6,-1],    [3,4,7,-1,1,5,3,6,-1,2,4,1,-1,7,3] (on garde le triangle supérieur qu'on "lit" ligne par ligne)
                           i->   [ 4, 5,-1, 2, 4, 1],                        + un sommet n'est pas voisin avec lui-même (diagonale de -1)
                                 [ 7, 3, 2,-1,-1, 7],
                                 [-1, 6, 4,-1,-1, 3],
                                 [ 1,-1, 1, 7, 3,-1]] 
                                            ^
                                            j               """

