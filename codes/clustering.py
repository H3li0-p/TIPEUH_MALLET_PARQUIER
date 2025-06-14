import numpy as np
import graph_carre as gc

def creer_tab_voisins(g,commandes):
    """Crée un dictionnaire à partir des sommets à visiter, les clés sont les sommets de la liste de commandes,
    et les valeurs associée sont une liste des autres sommets à visiter, par ordre croissant de distance au sommet courant"""
    tabvoisins = {}
    resto = g.get_resto()
    tabvoisins[resto] = [(v,gc.dist(g,resto,v)) for v in commandes]

    #print(tabvoisins)
    #print("")

    for u in commandes:
        tabvoisins[u] = []
        for v in commandes:
            if v != u:
                #print(v)
                tabvoisins[u].append((v,gc.dist(g,u,v)))
    for w in commandes:
        tabvoisins[w] = sorted(tabvoisins[w],key = lambda pt: pt[1])

    return tabvoisins

def DBSCA(graph,commandes,nb_max_elt,grain_depart,grain_div):
    """fait les groupes de livraison pour les commandes avec des groupes d'au plus nb_max_elt à partir de la liste de commandes, de graph, et d'un grain de départ"""
    #ne relancer que sur les groupes de trop grande taille
    #que contient commande ?
    liste_clust,to_check = DBSCA_classique(graph,commandes,nb_max_elt,grain_depart)
    if len(to_check) == 0:
        return liste_clust
    else:
        for elt in to_check:
            #print("elt ",elt)
            #print("")
            liste_finale = DBSCA(graph,elt,nb_max_elt,(grain_depart/grain_div),grain_div)
            liste_clust.extend(liste_finale)
        return liste_clust



#dbsca classique
def DBSCA_classique(graph,commandes,nb_max_elt,grain):
    out = []
    voisins = creer_tab_voisins(graph,commandes)
    visited = [0 for _ in range((graph.get_side_l())**2)]
    resto = graph.get_resto()
    visited[resto] = 1
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
    #print(voisins[sommet])
   # print("")
    i = 0
    acc_out =  []
    while (i < len(voisins[sommet])) and (voisins[sommet][i][1] < grain):
        if visited[voisins[sommet][i][0]] == 0: #si le sommet n'a pas été visité
            acc_out.extend(dbscarec(voisins[sommet][i][0],voisins,visited,grain))
        i += 1

    acc_out.append(sommet)
    return acc_out

def aux_n_v(ind,visited,out,nb_commandes,voisins):#à optimiser
    """construit la liste du parcours glouton naiv_parcours, sauf le dernier maillon entre le dernier indice et 0 (fait dans la fonction glouton_parcours - définition des variables dans la doc de la fonction glouton_parcours)"""
    visited[ind] = True
    #print("in boucle",out)
    if (len(out) == nb_commandes):
        return out
    else:
        for elt in voisins[ind]:
            if (visited[elt[0]] == False):
                out.append(elt[0])
                #print("a")
                return aux_n_v(elt[0],visited,out,nb_commandes,voisins)
        #print("b")
        out.append(ind)
        return out

def glouton_parcours(graph,command_list,start):
    """algo glouton génèrant à partir du couple (command_list,nb_commandes) (command_list = liste des commandes construite avec la fonction random_order + nb_commandes = le nombres de commandes soit le nombre de 1 dans la liste en excluant le resto (nb de 1 moins un) construit avec la fonction random_order) le parcours du plus proche voisin (0 = départ) dans l'objet UD_Graph graph.
    (!) pour l'instant ne marche que pour les graphes complets (nécessaire pour la récurence et la dernière ligne de code)"""
    #assert(graph.nb_vertices == len(command_tuple[0]))

    voisins = creer_tab_voisins(graph,command_list)
    nb_command = len(command_list)
    visited = {elt:False for elt in command_list}
    #print(nb_command)
    out = aux_n_v(start,visited,[start],(nb_command + 1),voisins)
    #print(out)
    a = out[-1:]
    out.append(start) #on prend le tout dernier sommet ajouté, et on le lie à start
    return out

def parcours_resto(graph,commandes,nb_livreurs,charge_max):
    """entree : liste de commandes, nb de livreurs, charge max en un parcours
sortie dictionnaire - clé numéro de livreur - liste de trajets à effectuer -[position resto - à visiter 1--- à visiter (n-1) - position resto]"""
    #etape1 = faire les clusters -heuristique de démarrage à préciser et à affiner
    n = graph.get_side_l()
    grain_depart = int(n/2)
    cluster = DBSCA(graph,commandes,charge_max,grain_depart,1.5)
    resto = graph.get_resto()

    #etape2 = pour chaque cluster, trouver le chemin à effectuer
    parcours = []
    for ind in range(len(cluster)):
        #print("c",cluster[ind])
        parc = glouton_parcours(graph,cluster[ind],resto)
        distance = gc.dist(graph,resto,parc[2])#on prend le premier sommet différent du resto
        parcours.append((ind,parc)) #à affiner en fct de la taille du cluster / de la distance

    parcours = sorted(parcours,key = lambda pt : pt[0])


    #dernière partie : attribution des clusters (que tout les plus loins ne soient pas pour le même livreur)
    #attribution d'un indice de distance à tout les clusters
    #tri des clusters en fct de l'indice décroissant
    #attribution en serpent des livreurs

    attribution_finale = {i:[] for i in range(nb_livreurs)}

    serpent_count = 0
    ind = 0
    while ind < len(parcours):#mise en place de la serpentation
        liv = 0
        while ((liv < nb_livreurs) and (ind < len(parcours))):
            if (serpent_count % 2 == 0): #on place à l'envers
                (attribution_finale[nb_livreurs - 1 - liv]).append(parcours[ind][1])
            else: #on place à l'endroit'
                (attribution_finale[liv]).append(parcours[ind][1])
            ind += 1
            liv += 1
        serpent_count += 1

    return attribution_finale


def test1():
    g = gc.graph_carre(10)
    g.set_restaurant(3,6)
    gc.verify(g,gc.test(g))

    cmds = gc.commandes_tab(g,17)
    print(creer_tab_voisins(g,cmds))

def test2():
    g = gc.graph_carre(10)
    g.set_restaurant(3,6)
    cmds = gc.commandes_tab(g,17)
    start = g.get_resto()
    print(glouton_parcours(g,cmds,start))
    print(start)

def test_serpent(nb_parcours,nb_livreurs):
    serpent_count = 0
    ind = 0
    while ind < nb_parcours: #mise en place de la serpentation
        for liv in range(nb_livreurs):
            if (serpent_count % 2 == 0): #on place à l'envers
                print(nb_livreurs - 1 - liv)
            else: #on place à l'endroit
                print(liv)
            ind += 1
        serpent_count += 1

def test3(nb_livreurs,charge_max):
    g = gc.graph_carre(10)
    g.set_restaurant(3,6)

    cmds = gc.commandes_tab(g,17)
    res = DBSCA(g,cmds,charge_max,5,1.5)
    #print("dbsca :",res)
    print(cmds)
    print(" ")
    dico = parcours_resto(g,cmds,nb_livreurs,charge_max)
    for ind in range(nb_livreurs):
        print(ind,":",dico[ind],"\n")

#test2()

#test_serpent(10,3)

test3(3,4)

def test4(nb_livreurs,capacity,size_city,resto,nb_commandes):
    print("///TEST TEMPS MOYEN///\n")
    g = gc.graph_carre(size_city)
    g.set_restaurant(resto[0],resto[1])

    cmds = gc.commandes_tab(g,nb_commandes)
    print(cmds,"\n")
    dico = parcours_resto(g,cmds,nb_livreurs,capacity)
    tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,10)
    for client in tmps_pr_maison.keys():
        print(client," : ",tmps_pr_maison[client],"\n")
    print(time_avg)

def test4bis(nb_livreurs,capacity,size_city,resto,nb_commandes):
    g = gc.graph_carre(size_city)
    g.set_restaurant(resto[0],resto[1])

    cmds = gc.commandes_tab(g,nb_commandes)

    dico = parcours_resto(g,cmds,nb_livreurs,capacity)
    tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,10)
    return time_avg






test4(3,3,10,(3,6),16)

def test_battery(n,nb_livreurs,charge_max,taille_ville,coos_resto,nb_commandes):
    """Lance n test à paramètres fixés et renvoie le temps moyen de livraison sur n simulation"""
    temps = []
    for _ in range(n):
        temps.append( test4bis(nb_livreurs,charge_max,taille_ville,coos_resto,nb_commandes))
    temps_np = np.array(temps)
    avg = np.mean(temps_np)
    incertitude = np.std(temps_np)/np.sqrt(n)
    return avg,incertitude

print(test_battery(1000,3,3,10,(3,6),16))
