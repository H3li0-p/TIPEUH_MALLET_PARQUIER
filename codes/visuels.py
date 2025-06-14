#pour un nombre de livreurs fixé, fait n tests avec des graphes / positions de restos aléatoires et récupère pour chaque simulation le temps moyen

#faire des probas - check cours maths - pour savoir quel est l'intervalle de confiance ? pas necessaire en fait si on a les barres d'erreur enft

#mettre des barres d'incertitude à tout les graphes

#graphe à réaliser : à nombre de commandes par soir fixé (dépendant des affluences réelles moyennes) pour une taille de graphe fixé (on essaye de prendre un truc représentant bien manhattan) et une charge fixée, on fait varier le nombre de livreurs, histoire d'avoir une idée du nombre de livreurs à avoir pour chaque situation

#pour des settings fixés (graphe + nb_livreurs + charge_max), faire varier le nombre de commandes pour voir la performance de l'algo sur beaucoup de commandes / peu de commandes plus ou moins éparses

def tab_graph_construction_nbliv(size_city,charge_max,nb_commandes,plage):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude du nombre nécessaires de livreurs - plage = nb max de livreurs avec lequel on va tester (inclus)"""
    x = []
    y = []
    yerrobar = []
    for i in range(1,(plage+1)):
        coord = (rd.randint(0,size_city),rd.randint(0,size_city))
        x.append(i)
        out = test_battery(nb_echantillons,i,charge_max,size_city,coord,nb_commandes)
        y.append(out[0])
        yerrorbar.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerrobar)
    return (outx,outy,outery)

def tab_graph_construction_cmax(size_city,nb_commandes,nb_livreurs,plage,nb_echantillons):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude de la variation de la charge max - plage = charge max on va tester (inclus)"""
    x = []
    y = []
    yerrobar = []
    for i in range(1,(plage+1)):
        coord = (rd.randint(0,size_city),rd.randint(0,size_city))
        x.append(i)
        out = test_battery(nb_echantillons,nb_livreurs,i,size_city,coord,nb_commandes)
        y.append(out[0])
        yerrorbar.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerrobar)
    return (outx,outy,outery)

def tab_graph_construction_nbcmds(size_city,charge_max,nb_livreurs,plage):
    """construit les deux tableaux nécessaires à la construction du graphe d'étude du nombre nécessaires de livreurs - plage ) nb max de livreurs avec lequel on va tester (inclus)"""
    x = []
    y = []
    yerrobar = []
    for i in range(1,(plage+1)):
        coord = (rd.randint(0,size_city),rd.randint(0,size_city))
        x.append(i)
        out = test_battery(nb_echantillons,nb_livreurs,charge_max,size_city,coord,i)
        y.append(out[0])
        yerrorbar.append(out[1])
    outx = np.array(x)
    outy = np.array(y)
    outery = np.array(yerrobar)
    return (outx,outy,outery)