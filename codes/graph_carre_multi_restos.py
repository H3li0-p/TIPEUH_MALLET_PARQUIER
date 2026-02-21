import random as rd

class cluster:

    def __init__(self):
        self.maisons = []
        self.repr = -1 #représentant non actualisé
        self.classement = [] #(numéro resto, distance)
        self.livré = False

    def livre(self):#permet de signaler quand le cluster est pris en charge
        self.livré = True

    def repr_calcul(self,side):
        len = len(self.maisons)
        if len == 0:
            raise(ValueError,"ce cluster est vide !")
        else:
            x = 0
            y = 0
            for elt in self.maisons:
                (xm,ym) = coords(side,i)
                x += xm
                y += ym
            return(x/len,y/len)

    def new_maisons(self,cl):
        self.maisons = cl

    def get_maisons(self):
        return self.maisons

    def sort_restos(self):
        l = self.classement
        self.classement = sorted(l,key = lambda x : x[1])

class resto:

    def __init__(self,co,ide):
        self.id = ide
        self.coords = co
        self.livreurs = []
        self.clusters = {} #indice : ordre de proximité - attribut : liste de clusters à cette position
        self.current = 0




class graph_carre:

    def __init__(self,n):
        self.side = n #immuable
        self.restaurant_liste = [] #restaurants numérotés de 0 à n-1,avec leur numéro de sommet
        #voir photo sur serveur discord pour savoir comment sont organisés les coordonées
        self.nb_livreurs = 0

    def get_side_l(self):
        return self.side

    def get_resto_liste(self):
        return self.restaurant_liste

    def get_nb_resto(self):
        return len(self.restaurant_liste)

    def modify_nb_livreurs(self,nb_liv):
        self.nb_livreurs = nb_liv

    def add_resto(self,x,y):
        (self.restaurant_liste).append(sommet(self.get_side_l(),x,y))

    def set_restaurant(self,nb,y,x):
        if (nb < len((self.restaurant_liste))):
            (self.restaurant_liste)[nb] = sommet(self.get_side_l(),y,x)
        else:
            raise(ValueError "ce restaurant n'existe pas !")

    def verify_livreurs(self):
        count = 0
        for elt in self.get_resto_liste():
            count += len(elt.livreurs)
        return (count == self.nb_livreurs)

def coords(side,u):
    """Obtiens les coordonnées du sommet u dans le graphe g (de côté side)"""
    return(u//side,u%side)

def sommet(side,y,x):
    """A partir des coordonées renvoie le sommet correspondant dans g (de côté side)"""
    side = g.get_side_l()
    if (x < side) and (y < side) and (0 < x) and (0 < y):
        return (side*y + x)
    else:
        raise(ValueError,"ce ne sont pas des coordonées valides !")

def dist(side,u,v):
    """Distance absolue entre 2 points"""
    xu,yu = coords(side,u)
    xv,yv = coords(side,v)
    return max(xu-xv,xv-xu) + max(yu-yv,yv-yu)

def dist_xy(side,u,v):
    """distance pour aller de u à v suivant x et y (algébrique)"""
    xu,yu = coords(side,u)
    xv,yv = coords(side,v)
    return xu-xv,yu-yv


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

def commandes_tab(g,n): #à oprimiser - ou forcer à prendre les derniers ?

    p = ((g.get_side_l())**2)
    assert(n < p) #sinon le programme ne termine pas

    commandes = []
    added = [False for _ in range(p)] #pour suivre les sommets déja sélectionnés

    for i in g.get_resto_liste():
        added[i] = True #pour ne pas que le resto soit un sommet sélectionné

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

def test_dico():
    tabtest = [1,2,3,5,6,7,8,9]
    print(dico_search(tabtest,4))
    print(dico_search(tabtest,1))
    print(dico_search(tabtest,9))
    print(dico_search(tabtest,-1))
    print(dico_search(tabtest,10))
    print(dico_search(tabtest,3))

g = graph_carre(7)
g.set_restaurant(0,5,4)
print(g.get_resto_liste())

l =[(1,0),(3,5),(4,2)]

#new ?