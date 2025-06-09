import clustering as cl
import graph_carre as gc

def DBSCA(graph,commandes,nb_max_elt,grain_depart,grain_div):
    """fait les groupes de livraison pour les commandes avec des groupes d'au plus nb_max_elt à partir de la liste de commandes, de graph, et d'un grain de départ"""
    #ne relancer que sur les groupes de trop grande taille
    #que contient commande ?
    liste_clust,to_check = DBSCA_classique(graph,commandes,nb_max_elt,grain_depart)
    if len(to_check) == 0:
        return liste_clust
    else:
        for elt in to_check:
            liste_finale = DBSCA(graph,elt,nb_max_elt,(grain_depart/grain_div),grain_div)
            liste_clust.extend(liste_finale)
        return liste_clust



#dbsca classique
def DBSCA_classique(graph,commandes,nb_max_elt,grain):
    out = []
    voisins = cl.creer_tab_voisins(graph,commandes)
    visited = [0 for _ in range((graph.get_side_l())**2)]
    to_recheck = [] #indice des clusters surs lequels relancer le dbsca
    for elt in voisins.keys():
        #print(elt)
        if visited[elt] == 0:
            #visited[elt] = 1
            cluster = dbscarec(elt,voisins,visited,grain)
            if len(cluster) > nb_max_elt:
                to_recheck.append(cluster)
            else:
                out.append(cluster)
    return (out,to_recheck)

#dbscarec
def dbscarec(sommet,voisins,visited,grain):
    visited[sommet] = 1 #surveiller la propagation de visited dans les appels rec
    #print(sommet)
    i = 0
    acc_out =  []
    while (i < len(voisins[sommet])) and (voisins[sommet][i][1] < grain):
        if visited[voisins[sommet][i][0]] == 0: #si le sommet n'a pas été visité
            acc_out.extend(dbscarec(voisins[sommet][i][0],voisins,visited,grain))
        i += 1

    acc_out.append(sommet)
    return acc_out

g = gc.graph_carre(20)
g.set_restaurant(3,6)

cmds = gc.commandes_tab(g,30)
print(DBSCA(g,cmds,5,6,2))