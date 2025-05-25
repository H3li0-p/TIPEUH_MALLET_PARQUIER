class graph_carre:
    
    def __init__(self,n):
        self.side = n
        self.mat = [[i for i in range(n)] for _ in range(n)]
        self.restaurant = 0

    def get_mat(self):
        return self.mat

    def get_side_l(self):
        return self.side

    def set_restaurant(self,x,y):
        self.restaurant = self.mat[x][y]


def coords(g,u):
    """Obtiens les coordonnées du sommet u dans le graphe g"""
    n = g.get_side_l
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
        

def trajet(g,u,v,w):
    """ "bruteforce" le meilleur trajet pour livrer 3 clients"""

    return 
