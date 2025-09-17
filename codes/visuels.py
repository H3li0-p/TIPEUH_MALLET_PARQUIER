#pour un nombre de livreurs fixé, fait n tests avec des graphes / positions de restos aléatoires et récupère pour chaque simulation le temps moyen

#faire des probas - check cours maths - pour savoir quel est l'intervalle de confiance ? pas necessaire en fait si on a les barres d'erreur enft

#mettre des barres d'incertitude à tout les graphes

#graphe à réaliser : à nombre de commandes par soir fixé (dépendant des affluences réelles moyennes) pour une taille de graphe fixé (on essaye de prendre un truc représentant bien manhattan) et une charge fixée, on fait varier le nombre de livreurs, histoire d'avoir une idée du nombre de livreurs à avoir pour chaque situation

#pour des settings fixés (graphe + nb_livreurs + charge_max), faire varier le nombre de commandes pour voir la performance de l'algo sur beaucoup de commandes / peu de commandes plus ou moins éparses

import time as t
import clustering as cl
import random as rd
import numpy as np
import matplotlib.pyplot as plt

def tab_graph_construction_nbliv(size_city,charge_max,nb_commandes,plage,nb_echantillons):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude du nombre nécessaires de livreurs - plage = nb max de livreurs avec lequel on va tester (inclus)"""
    x = []
    y = []
    yerr = []
    for i in range(1,(plage+1)):
        print("nb liveurs :",i)
        coord = (rd.randint(0,size_city-1),rd.randint(0,size_city-1))
        x.append(i)
        out = cl.test_battery(nb_echantillons,i,charge_max,size_city,coord,nb_commandes)
        y.append(out[0])
        yerr.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerr)
    return (outx,outy,outery)

def tab_graph_construction_cmax(size_city,nb_commandes,nb_livreurs,plage,nb_echantillons):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude de la variation de la charge max - plage = charge max on va tester (inclus)"""
    x = []
    y = []
    yerr = []
    for i in range(1,(plage+1)):
        print("charge max :",i)
        coord = (rd.randint(0,size_city),rd.randint(0,size_city))
        x.append(i)
        out = cl.test_battery(nb_echantillons,nb_livreurs,i,size_city,coord,nb_commandes)
        y.append(out[0])
        yerr.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerr)
    return (outx,outy,outery)

def tab_graph_construction_nbcmds(size_city,charge_max,nb_livreurs,plage,nb_echantillons):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude de l'évolution du nb de commandes  - plage ) nb max de commandes avec lequel on va tester (inclus)"""
    x = []
    y = []
    yerrobar = []
    for i in range(1,(plage+1)):
        print("nb commandes :",i)
        coord = (size_city//2,size_city//2)
        x.append(i)
        out = cl.test_battery(nb_echantillons,nb_livreurs,charge_max,size_city,coord,i)
        y.append(out[0])
        yerrorbar.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerrobar)
    return (outx,outy,outery)

def tab_graph_construction_nbech(size_city,charge_max,nb_commandes,nb_livreurs,plage):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude du nombre nécessaires d'échantillons - plage = nb max d'échantillons avec lequel on va tester (inclus)"""
    x = []
    y = []
    yerr = []

    temps = []
    for i in range(plage+1):
        print(i)
        temps.append(cl.test4bis(nb_livreurs,charge_max,size_city, (size_city//2,size_city//2),nb_commandes))
        temps_np = np.array(temps)
        avg = np.mean(temps_np)
        incertitude = np.std(temps_np)/np.sqrt(i)
        x.append(i)
        y.append(avg)
        yerr.append(incertitude)

    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerr)
    return (outx,outy,outery)

test1 = tab_graph_construction_nbech(100,10,100,10,500)
test2 = tab_graph_construction_nbech(100,10,100,10,500)
test3 = tab_graph_construction_nbech(100,10,100,10,500)
#print(test1)

plt.plot(test1[0],test1[1],'xr')
plt.plot(test2[0],test2[1],'xg')
plt.plot(test3[0],test3[1],'xb')
plt.show()
