import random as rd


class wgraph_carre:

    def __init__(self,n,maxD):
        self.side = n
        self.dmax = maxD
        self.mat = [[(k*n + i) for i in range(n*n)] for k in range(n*n)]
        self.dist = ([ [ (1 if i!=j else 0 ) for j in range(n*n)] for i in range(n*n)],False)
        self.restaurant = 0
       
    def get_mat(self):
        return self.mat
    
    def set_dist(self): #initialise la matrice des distances
        D = self.dist[0]
        s = self.side
        n = s*s
        # nombre de sommets
        dmax = self.dmax
        
        for i in range(n):
            for j in range(i):
                d = 1e9
                if (j == i + 1) or (j == i-1): #voisin de droite ou de gauche de i
                    if (j//s== i//s): #on vérifie que j est bien voisin de i, i.e ils sont sur la même ligne (cas i au "bord" du graphe)
                        d = rd.randint(1,dmax)
                elif (j == i - s) or (j == i + s): #voisin du dessus ou dessous de i
                    if (0<=j<n):
                        d = rd.randint(1,dmax)
                D[i][j] = (i!=j) * d
                D[j][i] = D[i][j]
        self.dist = (D,True)
                
    def get_dist(self):
        if not (self.dist[1]):
            self.set_dist()
        return self.dist[0]
    
    def get_side_l(self):
        return self.side

    def get_resto(self):
        return self.restaurant

    def set_restaurant(self,x,y):
        try:
            self.restaurant = self.mat[x][y]
        except:
            print("Failed to define restaurant (out of range)")

def floyd_warshall(g): #Implémentation de l'algorithme de floyd-warhshall
    s = g.get_side_l()
    n =  s*s #nombre de sommets du graphe 
    distance = g.get_dist()#Matrice des distances entre les sommets
    prev = [[0 for _ in range(n)] for _ in range(n)] #matrice gardant en mémoire, pour chaque couple de sommets (i,j), quel est le dernier sommet k du chemin i ->* j tel que la distance pour ce chemin soit la plus courte possible

    for k in range(n):
        for i in range(n):
            for j in range(n):
                d1 = distance[i][j]
                d2 = distance[i][k] + distance[k][j]
                
                distance[i][j] = min(d1,d2)
                
    return distance


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