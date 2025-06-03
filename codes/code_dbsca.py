## Classes - objets

import numpy as np
import random as rd
import matplotlib.pyplot as plt

class Point:

    def __init__(self,x0,y0):
        self.x = x0
        self.y = y0

    def distance(self,point):
        return (np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2))

    def __str__(self):
        return str(self.x) + " " + str(self.y)

#D = {A(point):true(vérifié ou non)}

d = {'a':1,'ab':2,'gh':3}


## fontcions

def construction_voisins_naif(p:Point,D:dict,epsi:float):
    out = []
    card = 0
    for elt in D.keys():
        if (elt == p):
            continue
        elif (p.distance(elt) <= epsi):
            out.append(elt)
            card += 1
    return out, card

def calculer_C(p:Point, C:set, D:dict, minPt:int, epsi:float, out:dict):
    N, card = construction_voisins_naif(p,D,epsi)
    C.add(p)
    if (card < minPt):
        out[0].append(p) #0 - cluster du bruit
        D[p]=True
    else:
        D[p]=True
        for elt in N:
            #C.append(elt)
            if False == D[elt]:
                C |= calculer_C(elt,C,D,minPt,epsi,out)
    return C

def DBSCAN(D:dict,minPt:int,epsi:float):
    out = {}
    i = 0
    for elt in D.keys():
        N, card = construction_voisins_naif(elt,D,epsi)
        
        if (card < minPt):
            out[0].append(elt)
        else:
            i += 1
            c = {elt}
            for p in N:
                c |= calculer_C(p,{elt},D,minPt,epsi,out)
            out[i] = c
    return out

## génération d'un nuage de points

def generation_pts(nb:int,xrange:float,yrange:float): #genere un nuage de point aleatoires avec des coordonnes comprises pour x entre 0 et xrange, pour y entre 0 et yrange
    assert(nb > 0)
    rd.seed(None)
    out= {}
    for i in range(0,nb):
        i = Point(rd.uniform(0.0,xrange),rd.uniform(0.0,yrange))
        out[i]=False
        #print(i)
    return out

test1 = generation_pts(100,100,100)
for pt in test1 :
    print(pt.__str__())    
## affichage
dict1 = DBSCAN(test1,2,1000)

def printf_cluster(l):
    x = []
    y = []
    for elt in l:
        x.append(elt.x)
        y.append(elt.y)
    plt.scatter(x,y)

def print_dico_res(D):
    for elt in D.keys():
        printf_cluster(D[elt])
    plt.show()


for elt in test1.keys():
    N,d = construction_voisins_naif(elt,test1,105)
    #printf_cluster(N)
    
print_dico_res(dict1)