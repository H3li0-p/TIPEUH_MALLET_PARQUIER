import random as rd


class graph_carre:

    def __init__(self,n):
        self.side = n
        self.mat = [[(k*n + i) for i in range(n)] for k in range(n)] #? intéret ?
        self.restaurant = 0

    def get_mat(self):
        return self.mat

    def get_side_l(self):
        return self.side

    def get_resto(self):
        return self.restaurant

    def set_restaurant(self,x,y):
        try:
            self.restaurant = self.mat[x][y]
        except:
            print("Failed to define restaurant (out of range)")

def coords(g,u):
    """Obtiens les coordonnées du sommet u dans le graphe g"""
    n = g.get_side_l()
    return(u//n,u%n)

def sommet(g,x,y):
    """Obtiens un sommet de g à partir de ses coordonnées"""
    mat = g.get_mat()
    try:
        return (mat[x][y])
    except:
        print("Error, vertex not in graph")
        return -1
    

def dist(g,u,v):
    """Distance absolue entre 2 points"""
    xu,yu = coords(g,u)
    xv,yv = coords(g,v)
    return max(xu-xv,xv-xu) + max(yu-yv,yv-yu)

def dist_xy(g,u,v):
    """distance pour aller de u à v suivant x et y (algébrique)"""
    xu,yu = coords(g,u)
    xv,yv = coords(g,v)
    return xu-xv,yu-yv


def dist_chemin(g,path):
    i = 0
    d = dist(g,g.get_resto(),path[0])
    while (i < len(path)-1):
        d += dist(g,path[i],path[i+1])
        i+=1
    return d

def permutations(maisons):
    """calcule les 3! = 6 trajets possible pour relier 3 maisons : le coût est en 0(n!) mais cette fonction sera toujours appliquée pour 3 éléments seulement"""
    n = len(maisons)
    p = [maisons]
    for k in range(0,n-1):
        for i in range(0, len(p)):
            z = p[i][:]
            for c in range(0,n-k-1):
                z.append(z.pop(k))
                if (z not in p):
                    p.append(z[:])
    return p


def trajet(g,maisons):
    """ "bruteforce" le meilleur trajet pour livrer 3 clients"""
    out = []
    paths = permutations(maisons)
    d = [dist_chemin(g,s) for s in paths]
    out = paths[d.index(min(d))]
    return out

def test(g):
    n = (g.get_side_l()**2)-1
    commandes = []
    u = rd.randint(0,n)
    for i in range(3):
        while u in commandes or u == g.get_resto():
            u = rd.randint(0,n)

        commandes.append(u)
    chemin = trajet(g,commandes)
    return chemin

def verify(g,res):
    print(res)
    for i in permutations(res):
        print(i,dist_chemin(g,i))

def insert_sorted(liste,elt):
    """insertion d'un elt dans une liste triée par ordre croissant"""
    n = len(liste)
    liste.append(elt)
    #print(liste[n])
    while (n>0) and (elt <= liste[n-1]): # pas a la bonne place par rapport à l'elt d'avant
        liste[n] = liste[n -1]  #decalage de un terme
        #print(liste)
        n -= 1
        #print(n)
    liste[n] = elt

def commandes_tab(g,n): #à oprimiser - ou forcer à prendre les derniers ? = non, cela conduirait à une non uniformité deschances de tiret tel ou tel sommet

    p = ((g.get_side_l())**2)
    assert(n < p) #sinon le programme ne termine pas

    commandes = []
    added = [False for _ in range(p)] #pour suivre les sommets déja sélectionnés
    added[g.get_resto()] = True #pour ne pas que le resto soit un sommet sélectionné
    u = rd.randint(0,p-1)
    for i in range(n):
        while added[u]:
            u = rd.randint(0,p-1)
        added[u] = True
        insert_sorted(commandes,u)
    return commandes

def time_to_deliver(g,attrib,longueur,vitesse):
    """On suppose que la vitesse des livreurs est constante et identique pour chaque livreur (ce sont des pros)"""
    """Renvoie pour chaque sommet à visiter du graphe (client à visiter) le temps de livraison de ce client ainsi que le temps moyen de livraison"""
    temps_par_maison = {}
    resto = g.get_resto()
    time = 0
    for livreur in attrib.keys():
        itineraire = attrib[livreur]
        #print(livreur,":",itineraire)
        tps = 0
        for groupes in itineraire:
            current = resto
            for client in groupes:
                tps += dist(g,current,client)*longueur/vitesse

                if client != resto:
                    temps_par_maison[client] = tps

                time += tps
                current = client

    return temps_par_maison,time/len(temps_par_maison)

g = graph_carre(10)
print(commandes_tab(g,10))

def test_dico():
    tabtest = [1,2,3,5,6,7,8,9]
    print(dico_search(tabtest,4))
    print(dico_search(tabtest,1))
    print(dico_search(tabtest,9))
    print(dico_search(tabtest,-1))
    print(dico_search(tabtest,10))
    print(dico_search(tabtest,3))

#insert_sorted(tabtest,-1)
#print(tabtest)
