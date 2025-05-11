#Graphes non-orienté
import random as rd

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
    self.voisins de la forme [numéro sommet, distance]
    """
    def offset_mat_lin(self,u,v):
        """calcule l'offset entre les sommets i et j pour la matrice linéarisé"""
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
                self.voisins[u].insert(mid,[v,weight])
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


    def get_voisins_mat(self):
        return self.voisins
        
    def get_voisins(self,u):
        return self.voisins[u]
    
    def get_edge(self,u,v):
        """renvoie la valeur de l'arête entre u et v"""
        return self.mat_lin[self.offset_mat_lin(u,v)]
        
    def __str__(self):
        print("nb vertices :",self.nb_vertices)
        print("nb edges",self.nb_edges)
        print("listes d'adjacence")
        
        for i in range(self.nb_vertices):
            print("sommet :",i,self.voisins[i])
        
        print("matrice d'adjacence ( du sommet 0 au sommet",(self.nb_vertices),") - (!) la diagonale n'est pas affiché ! (pas de boucles possibles = on commence au lien entre le sommet 0 et 1\n")
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

def random_perfect_graph(n,max):
    """créer un graphe aléatoire complet à n sommets dont les poids des arrêtes sont compris entre 1 et max"""
    assert(max >= 1)
    assert(n>=2)
    
    out = UD_Graph(n)
    for i in range(n):
        for j in range(i+1,n):
            out.add_edge(i,j,rd.uniform(0.1,max))
    return out

objet2 = random_perfect_graph(10,30)
#print(objet2)

def random_order(graph):
    """à partir d'un objet de classe UD_graph, génère une liste aléatoire de 0 et de 1 de longueur égale au nombre de sommets(1 = demandant une commande / 0 = ne demande pas de commande) (!) la case 0 est toujours à 1 car considéré comme le restaurant donc doit toujours être inclu dans le cycle"""
    nv = graph.nb_vertices
    nb_commandes = 0 #exclu le restaurant
    out = [1] #restaurant considéré comme 0 => toujours à 1 (pour être pris en compte dans la boucle)
    for _ in range(1,nv):
        order = rd.randint(0,1)
        nb_commandes += order
        out.append(order)
    return (out,nb_commandes)

#print(random_order(objet2))
"""on choisi arbitrairement le graphe 0 comme le graphe du restaurant"""

def aux_n_v(graph,ind,command_list,out,nb_commandes):
    """construit la liste du parcours glouton naiv_parcours, sauf le dernier maillon entre le dernier indice et 0 (fait dans la fonction glouton_parcours - définition des variables dans la doc de la fonction glouton_parcours)"""
    print(out)
    command_list[ind] = 0
    if (len(out) == nb_commandes):
        return out
    else:
        for elt in graph.get_voisins(ind):
            if (command_list[elt[0]] == 1):
                return aux_n_v(graph,(elt[0]),command_list,(out.append([ind,elt[0]])),nb_commandes)

def glouton_parcours(graph,command_tuple):
    """algo glouton génèrant à partir du couple (command_list,nb_commandes) (command_list = liste des commandes construite avec la fonction random_order + nb_commandes = le nombres de commandes soit le nombre de 1 dans la liste en excluant le resto (nb de 1 moins un) construit avec la fonction random_order) le parcours du plus proche voisin (0 = départ) dans l'objet UD_Graph graph.
    /!\ pour l'instant ne marche que pour les graphes complets (nécessaire pour la récurence et la dernière ligne de code)
    /!\ ne donne que les sommets à suivre et non la distance, va être nécessaire"""
    print(len(command_tuple[0]))
    assert(graph.nb_vertices == len(command_tuple[0]))
    
    out = aux_n_v(graph,0,command_tuple[0],[],command_tuple[1])
    out.append([(out[-1:][1]),0]) #on prend le tout dernier sommet ajouté, et on le lie à 0 -> possible car graphe complet !
    
    """out = [] #initialiser avec la prelière valeur non nulle
    last_ind = 0
    for i in range(graph.nb_vertices):
        if command_list[i] == 1:
            last_ind = i
            command_list[i] = 0
            for elt in (graph.get_voisins())[i]:
                if command_list[elt[0]] == 1: #si le somm
                    command_list[elt[0]] == 0
                    out.append(elt)
                    print(i)
                    break
    # /!\ à cause de cetgte dernière ligne, ne marche que pour les graphes complets (on n'est pas surs de l'existence entre la denière arrête et le sommet de départ)
    out.append([0,graph.get_edge(last_ind,0)])"""
    return out

objet3 = random_perfect_graph(20,30)
test3 = random_order(objet3)
print("originlist",test3)
print(glouton_parcours(objet3,test3))