"""Graphes non-orienté """
class Graph :
    
    def __init__(self,nv):     

        self.nb_edges = 0
        self.mat = [[-1 for _ in range(nv)] for _ in range(nv)]
        self.nb_vertices = nv
        self.mat_lin = [-1 for _ in range((nv*(nv-1))/2)] #version linéarisée de la matrice d'adjacence
        self.voisins = [[] for _ in range(nv)]


                            """[ [-1, 3, 4, 7,-1, 1], exemple de matrice complète, la linéarisation donnerait: 
                                 [ 3,-1, 5, 3, 6,-1],    [3,4,7,-1,1,5,3,6,-1,2,4,1,-1,7,3] (on garde le triangle supérieur qu'on "lit" ligne par ligne)
                           i->   [ 4, 5,-1, 2, 4, 1],                        + un sommet n'est pas voisin avec lui-même (diagonale de -1)
                                 [ 7, 3, 2,-1,-1, 7],
                                 [-1, 6, 4,-1,-1, 3],
                                 [ 1,-1, 1, 7, 3,-1]] 
                                            ^
                                            j               """

    
    def update_mat_lin(self,u,v,w):
        """met les champs à jour lors de l'ajout/suppression d'un arc"""
        nv = self.nb_vertices
        i = min(u,v)
        j = max(u,v)
        self.mat_lin["""calcul d'indice pour mat triangle sup"""] = w 
       
    def update_voisins(self,u,v,w):
        nv = self.nb_vertices
        voisins_u = self.voisins[u]
        voisins_u.append(v)
        nb_nb = len(voisins_u)
        debut = 0
        fin = nb_nb

        mat_lin = self.mat_lin
        i = min(u,v)
        j = max(u,v)

        """idée : insertion dichotomique dans la liste des voisins (qui est déjà triée)"""
        #utiliser : voisins_u = voisins_u[:a] + [j] + voisins_u[a:] ?


    def add_edge(self,u,v,float weight):
        """Ajout d'une arrête entre les sommets u et v"""
        nv = self.nb_vertices
        assert (weight > 0),"Distance invalide"
        assert (u!=v),"Pas de boucles (sommets identiques"
        assert (u<nv and v < nv), "InvalidVertices"

        self.update_mat_lin(u,v,weight)
        self.update_voisins(u,v,weight)

    def remove_edge(self,u,v):

    def get_voisins(self):
        return self.voisins

    def get_lin_adj(self):
        return self.mat_lin





