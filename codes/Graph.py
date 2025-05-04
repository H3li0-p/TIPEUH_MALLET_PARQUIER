"""Graphes non-orienté """
class UD_Graph : #UD pour undirected
    
    def __init__(self,nv): #int pour nv = le nb de sommets    
        self.nb_edges = 0
        assert(nv > 1)
        #self.mat = [[-1 for _ in range(nv)] for _ in range(nv)]
        self.nb_vertices = nv
        self.mat_lin = [-1 for _ in range(int((nv*(nv-1))/2))] #version linéarisée de la matrice d'adjacence
        self.voisins = [[] for _ in range(nv)] #couple (indice du sommet (entier),valeur (float))

    """                               [ [-1, 3, 4, 7,-1, 1], exemple de matrice complète, la linéarisation donnerait: 
                                    [ 3,-1, 5, 3, 6,-1],    [3,4,7,-1,1,5,3,6,-1,2,4,1,-1,7,3] (on garde le triangle supérieur qu'on "lit" ligne par ligne)
                            i->   [ 4, 5,-1, 2, 4, 1],                        + un sommet n'est pas voisin avec lui-même (diagonale de -1)
                                    [ 7, 3, 2,-1,-1, 7],
                                    [-1, 6, 4,-1,-1, 3],
                                    [ 1,-1, 1, 7, 3,-1]] 
                                                ^
                                                j               
    """
    def offset_mat_lin(self,u,v):
        nv = self.nb_vertices
        #assert (u < self.nb_vertices and v < self.nb_vertices), "InvalidVertices"
        
        i = min(u,v)
        j = max(u,v)
        ind = j-1-i
        for k in range(i):
            ind += (nv-k-1)
        return ind
        
        
    def update_mat_lin(self,u,v,w):
        """met les champs à jour lors de l'ajout/suppression d'un arc"""
        nv = self.nb_vertices
        self.mat_lin[self.offset_mat_lin(u,v)] = w 


    def voisins_dico_insert(self, u, v, weight, borninf, bornsup): #à tester
        """effectue une insertion dicotomique de v dans les voisins de u entre borninf et bornsup inclus à partir du poids. #(enlevé : Renvoie true si l'ajout a bien eu lieu, false sinon)
        -> b = true <=> ajout/modif de l'arrête ente u et v
        -> b = false <=> supression de l'arrête entre u et v"""
        
        assert (u < self.nb_vertices and v < self.nb_vertices), "InvalidVertices"
        assert (borninf >= 0), "borne inf invalide !"
        assert (bornsup < len(self.voisins[u])), "borne sup invalide !"
        mid = 0
       # print(borninf,bornsup)
        
        while(borninf <= bornsup):
            mid = int((borninf + bornsup) / 2)
           # print(mid)
            current = self.voisins[u][mid][1]
           # print(current)
            if (current == weight):
                self.voisins[u].insert(mid,(v,weight))
                return True
            elif (current < weight):
                borninf = mid + 1 
            else:
                bornsup = mid - 1

        mid = int((borninf + bornsup + 1) / 2)
        self.voisins[u].insert(mid,[v,weight]) 
        #print("a",mid,weight)#à optim en c
        return False
    
    def voisins_modif(self,u,v,weight,b):
        """modifie / enlève l'arête associé à v de la liste des voisins de u
        -> b = true : modification
        -> b = false : supression"""
        assert (u < self.nb_vertices and v < self.nb_vertices), "InvalidVertices"
        
        i = 0
        
        while i < (len(self.voisins[u])):
            if (self.voisins[u][i][0] == v):
                if b:
                    self.voisins[u][i][1] = weight
                else:
                    bu = self.voisins[u].pop(i)
                i = len(self.voisins[u])
            i += 1
    
    def update_voisins(self,u,v,w,b):
        """ met à jour la liste des voisins d'un graphe
        b est un booléen qui permet de savoir si c'est un ajout/mise à jour ou une supression
        ajout -> b = true
        supression -> b = false"""
        
        if b:
            if (self.mat_lin[self.offset_mat_lin(u,v)] != -1):
                self.voisins_modif(u,v,w,True) #ne sont pas triés selon les sommets = on ne peut pas les avoir via dicotomie mais par un parcours lambda de liste
                return False
            else:
                self.voisins_dico_insert(u,v,w,0,(len(self.voisins[u]) - 1))
                return True
        else:
            if (self.mat_lin[self.offset_mat_lin(u,v)] != -1):
                self.voisins_modif(u,v,w,False)
                return True
            else:
                return False

        """idée : insertion dichotomique dans la liste des voisins (qui est déjà triée)""" #bonne idée !

        #utiliser : voisins_u = voisins_u[:a] + [j] + voisins_u[a:] ?


    def add_edge(self,u,v,weight):
        """Ajout d'une arrête entre les sommets u et v"""
        nv = self.nb_vertices
        assert (weight > 0),"Distance invalide"
        assert (u!=v),"Pas de boucles (sommets identiques"
        assert (u < nv and v < nv), "InvalidVertices"

        b = self.update_voisins(u,v,weight,True)
        self.update_voisins(v,u,weight,True)
        self.update_mat_lin(u,v,weight)
        
        if b:
            self.nb_edges += 1

    def remove_edge(self,u,v):
        """supression d'une arrête entre les sommets u et v"""
        nv = self.nb_vertices
        assert (u!=v),"Pas de boucles (sommets identiques)"
        assert (u<nv and v < nv), "InvalidVertices"

        b = self.update_voisins(u,v,-1,False)
        self.update_voisins(v,u,-1,False)
        self.update_mat_lin(u,v,-1)
        if b:
            self.nb_edges -= 1


    def get_voisins(self):
        return self.voisins

    def get_lin_adj(self):
        return self.mat_lin
        
    def __str__(self):
        print("nb vertices :",self.nb_vertices)
        print("nb edges",self.nb_edges)
        print("listes d'adjacence")
        
        for i in range(self.nb_vertices):
            print("sommet :",i,self.voisins[i])
        
        print("matrice d'adjacence ( du sommet 0 au sommet",(self.nb_vertices),") - /!\ la diagonale n'est pas affiché ! (pas de boucles possibles = on commence au lien entre le sommet 0 et 1\n")
        for j in range(self.nb_vertices-1):
            print("   ,"*j,"  ",self.mat_lin[self.offset_mat_lin(j,j+1):self.offset_mat_lin(j+1,j+2)])
            """ a = self.mat_lin[(self.offset_mat_lin(j-1,0)):(self.offset_mat_lin(j,0))]
            print((self.offset_mat_lin(j-1,0)),(self.offset_mat_lin(j,0)))
            print(a)"""
        return""
        
    #à implémenter en c : supression d'un objet graphe

def test1():
    objet1 = UD_Graph(5)
    objet1.add_edge(0,2,22.2)
    objet1.add_edge(0,3,258.3)
    objet1.add_edge(0,1,0.5)
    objet1.add_edge(0,4,33.2)
    print(objet1)
    print("\n")
    
    objet1.add_edge(0,2,38.2)
    objet1.add_edge(0,1,1)
    objet1.remove_edge(0,3)
    objet1.remove_edge(1,3)
    objet1.add_edge(3,4,85.2)
    print(objet1)

#test1()

