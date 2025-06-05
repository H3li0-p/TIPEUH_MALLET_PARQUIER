import random as rd


class graph_carre:
    
    def __init__(self,n):
        self.side = n
        self.mat = [[(k*n + i) for i in range(n)] for k in range(n)]
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
    chemin = trajet(g,commandes[0],commandes[1],commandes[2])
    return chemin

def verify(g,res):
    print(res)
    for i in permutations(res[0],res[1],res[2]):
        print(i,dist_chemin(g,i))


def commandes_tab(g,n):
    p = (g.get_side_l()**2)-1
    u = rd.randint(0,p)
    commandes = []
    for i in range(n):
        while u in commandes or u == g.get_resto():
            u = rd.randint(0,p)
        commandes.append(u)
    return commandes



