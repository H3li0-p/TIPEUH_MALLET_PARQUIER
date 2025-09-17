import numpy as np
import graph_carre as gc

def nth_root(a,n):
    return np.power(a,(1/n))

def nouveau_grain(grain,ch_max,nb):
    """Permet un calcul plus fin du grain lors des appels récursif du dbsca"""
    #A n'utiliser que si le grain est supérieur à 1
    assert(grain > 1)
    return int(np.floor(nth_root(nb/ch_max,n_rate)))

def dico_search(tab,elt):
    """effectue une recherche dichotomique dans la liste de elt, et renvoie True si elle est présente, False sinon"""
    inf = 0
    sup = len(tab)
    while (inf <= sup): #tant qu'il reste une fenetre a etudier
        mid = int((inf + sup)/2)
        if (mid >= len(tab)):
            return False
        elif (tab[mid] == elt):
            return True
        elif (tab[mid] < elt): #dans la partie supérieure du tableau
            inf = mid + 1
        else: #sinon dans la partie inferieure
            sup = mid - 1
    #l'elt n'a pas ete trouve
    return False

def creer_tab_voisins(g,commandes): #0(n^2ln(n)) avec n = nb commandes
    """Crée un dictionnaire à partir des sommets à visiter, les clés sont les sommets de la liste de commandes,
    et les valeurs associée sont une liste des autres sommets à visiter, par ordre croissant de distance au sommet courant"""
    tabvoisins = {}
    resto = g.get_resto()
    tabvoisins[resto] = [(v,gc.dist(g,resto,v)) for v in commandes] #création de la liste du restaurant (pas dans la liste des commandes mais non nécessaire)

    for u in commandes:#pour tout les sommets
        tabvoisins[u] = []
        for v in commandes:
            if v != u:
                tabvoisins[u].append((v,gc.dist(g,u,v))) #on récupère la distance à tout les sommets
    for w in commandes:
        tabvoisins[w] = sorted(tabvoisins[w],key = lambda pt: pt[1]) #on trie tout les sommets par distance

    return tabvoisins

def filtrage_voisins(commandes_base,voisins_complet,resto,g): #complexité en n^2, n^3 au pire à cause du in
    """filtre le dictionnaire général des voisins selon la liste de commande et renvoie un dictionnaire réduit correspondant
    resto = False : ne conserve pas les coordonées du resto
    resto = True : conserve les coordonées du resto"""
    voisins = {}
    commandes = commandes_base.copy()
    if resto: #si on a besoin de la distance au resto
        r = g.get_resto()
        gc.insert_sorted(commandes,r)

    #nettoyage de la table des voisins
    for elt in commandes:
        #print(elt)
        tmp = (voisins_complet[elt]).copy()
        voisins[elt] = tmp
        #print("voisins[elt]",voisins[elt],"\n")
        ind = 0
        while ind < len(voisins[elt]): #on verifie que tout les points voisins de elt sont bien dans la liste de commandes
            pt = ((voisins[elt])[ind])
            t = dico_search(commandes,(pt[0]))
            if (pt[0]) in commandes:
                ind += 1
            else:
                l = voisins[elt]
                l.remove(pt)
                voisins[elt] = l

    return voisins

def DBSCA(graph,commandes,nb_max_elt,grain_depart, voisins): #fonction récursive
    """fait les groupes de livraison pour les commandes avec des groupes d'au plus nb_max_elt à partir de la liste de commandes, de graph, et d'un grain de départ"""
    #ne relancer que sur les groupes de trop grande taille
    #que contient commande ?

    liste_clust,to_check,v_new = DBSCA_classique(graph,commandes,nb_max_elt,grain_depart,voisins)
    if len(to_check) == 0:
        return liste_clust
    else:
        for elt in to_check:
            ##
            if (grain > 1):
                nb = len(elt)
                grain = nouveau_grain(grain_depart,nb_max_elt,nb)
                
                liste_finale = DBSCA(graph,elt,nb_max_elt,grain,v_new) #tant que les groupes sont trop grands, on relance le dbsca dessus de manière récursive
                liste_clust.extend(liste_finale)
            ##
            else:
            """Cas particulier grain = 1"""
        return liste_clust

#dbsca classique
def DBSCA_classique(graph, commandes, nb_max_elt, grain, voisins_complet): #n^2 (recursivité) + n^2 (filtrage du tableau)
    """graph : structure de donées de type graphe, représentant un graphe carré
    commandes : maisons à livrer
    voisins_complet ="""
    p = (graph.get_side_l())**2
    out = []
    """inutile au tour 1, a mettre en parametre"""
    voisins = filtrage_voisins(commandes,voisins_complet,False,graph) #on extrait de la grande table des voisins ce qui est necessaire

    visited = [0 for _ in range(p)] #permet de suivre quels sommets ont étés visités soit traités
    resto = graph.get_resto()
    visited[resto] = 1
    to_recheck = [] #indice des clusters sur lequels relancer le dbsca
    for elt in voisins.keys(): #boucle sur les cmds (n)
        if visited[elt] == 0: #si non visité
            cluster = dbscarec(elt,voisins,visited,grain) #génération du cluster par propagation récursive
            if len(cluster) > nb_max_elt: #si le cluster est trop grand
                to_recheck.append(cluster)
            else:
                out.append(cluster)
    return (out,to_recheck,voisins) #on récupère les groupes de bonne taille, les groupes trop grand, la table des voisins déjà filtré (permettra de filtrer sur plus petit)

#dbscarec
def dbscarec(sommet,voisins,visited,grain): #pire des cas - n sommets
    visited[sommet] = 1 #sommet visité
    i = 0
    acc_out = []
    while (i < len(voisins[sommet])) and (voisins[sommet][i][1] < grain): #tant que le sommet est en dessous du grain
        if visited[voisins[sommet][i][0]] == 0: #si le sommet n'a pas été visité
            acc_out.extend(dbscarec(voisins[sommet][i][0],voisins,visited,grain)) #on relance la récursivité dessus et on ajoute le résultat au cluster de sortie
        i += 1

    acc_out.append(sommet)
    return acc_out

def aux_n_v(ind,visited,out,nb_commandes,voisins):#à optimiser - n^2 (nb_commandes)
    """construit la liste du parcours glouton naiv_parcours, sauf le dernier maillon entre le dernier indice et 0 (fait dans la fonction glouton_parcours - définition des variables dans la doc de la fonction glouton_parcours)"""
    visited[ind] = True
    if (len(out) == nb_commandes): # = contient tout les sommets de la liste cluster car on ne peut pas avoir un sommet en double
        return out
    else:
        for elt in voisins[ind]: #pour tout les voisins
            if (visited[elt[0]] == False): #non visités
                out.append(elt[0])
                return aux_n_v(elt[0],visited,out,nb_commandes,voisins) #on rela,ce l'appel pour trouver le voisin le plus proche

        out.append(ind) #on ajoute le sommet courant
        return out

def glouton_parcours(graph,command_list,start, voisins_complet):
    """algo glouton génèrant à partir du couple (command_list,nb_commandes) (command_list = liste des commandes construite avec la fonction random_order + nb_commandes = le nombres de commandes soit le nombre de 1 dans la liste en excluant le resto (nb de 1 moins un) construit avec la fonction random_order) le parcours du plus proche voisin (0 = départ) dans l'objet UD_Graph graph.
    (!) pour l'instant ne marche que pour les graphes complets (nécessaire pour la récurence et la dernière ligne de code)"""
    #assert(graph.nb_vertices == len(command_tuple[0]))

    nb_command = len(command_list)
    voisins = filtrage_voisins(command_list,voisins_complet,True,graph) #création de la table voisin de référence

    visited = {elt:False for elt in command_list} #dictionnaire de suivi des sommets parcourus

    out = aux_n_v(start,visited,[start],(nb_command + 1),voisins) #parcours récursif des voisins pour construire le chemin de proche en proche

    out.append(start) #on prend le tout dernier sommet ajouté, et on le lie à start
    return out

def parcours_resto(graph,commandes,nb_livreurs,charge_max): #n^2ln(n) - DBSCA
    """entree : liste de commandes, nb de livreurs, charge max en un parcours
sortie dictionnaire - clé numéro de livreur - liste de trajets à effectuer -[position resto - à visiter 1--- à visiter (n-1) - position resto]"""

    #etape0 = generer la liste des voisins
    voisins = creer_tab_voisins(graph,commandes)

    #etape1 = faire les clusters - heuristique de démarrage à préciser et à affiner
    n = graph.get_side_l()
    grain_depart = int(n/2) #à affiner
    cluster = DBSCA(graph,commandes,charge_max,grain_depart,1.5,voisins)
    resto = graph.get_resto()

    #etape2 = pour chaque cluster, trouver le chemin à effectuer
    parcours = []
    for ind in range(len(cluster)):
        parc = glouton_parcours(graph,cluster[ind],resto,voisins)

        distance = gc.dist(graph,resto,parc[1]) #on prend le premier sommet différent du resto (c'est le plus proche)
        parcours.append((ind,parc)) #à affiner en fct de la taille du cluster / de la distance

    parcours = sorted(parcours,key = lambda pt : pt[0])

    #dernière partie : attribution des clusters (que tout les plus loins ne soient pas pour le même livreur)
    #attribution d'un indice de distance à tout les clusters (indice elevee = distance elevee)
    #tri des clusters en fct de l'indice décroissant
    #attribution en serpent des livreurs

    attribution_finale = {i:[] for i in range(nb_livreurs)}

    serpent_count = 0
    ind = 0
    while ind < len(parcours):#mise en place de la serpentation
        liv = 0
        while ((liv < nb_livreurs) and (ind < len(parcours))): #boucle sur le nombre de livreurs
            if (serpent_count % 2 == 0): #on attribue à l'envers (ordre décroissant)
                (attribution_finale[nb_livreurs - 1 - liv]).append(parcours[ind][1])
            else: #on attribue à l'endroit (ordre croissant)
                (attribution_finale[liv]).append(parcours[ind][1])
            ind += 1
            liv += 1
        serpent_count += 1 #donne l'ordre de la serpentation

    return attribution_finale

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

#test3(3,4)

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
    tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,9)
    return time_avg

#test4(3,3,10,(3,6),16)

def test_battery(n,nb_livreurs,charge_max,taille_ville,coos_resto,nb_commandes):
    """Lance n test à paramètres fixés et renvoie le temps moyen de livraison sur n simulation"""
    temps = []
    for _ in range(n):
        temps.append(test4bis(nb_livreurs,charge_max,taille_ville,coos_resto,nb_commandes))
    temps_np = np.array(temps)
    avg = np.mean(temps_np)
    incertitude = np.std(temps_np)/np.sqrt(n)
    return avg,incertitude

print(test_battery(1,3,3,10,(3,6),10))

def test():
    g = gc.graph_carre(10)
    g.set_restaurant(5,5)
    r = g.get_resto()
    print(r)

    commandes = [33, 41, 47, 48, 53, 79, 80, 82, 84, 95]
    print(commandes)

    parcours_resto(g,commandes,3,3)
    """
    v = creer_tab_voisins(g,commandes)
    a = commandes[0:5]
    b = commandes[0:2]
    print("\nvoisins o",v,"\n")
    voi = filtrage_voisins(a,v,False,g)
    print(a)
    print("\nvoisins_source t1",v)
    print("\nvoisinmodif",voi,"\n")
    voi = filtrage_voisins(b,v,True,g)
    print(b,"\n")
    print("\nvoisins_source t2",v)
    print("\nvoisinmodif",voi)
    """

#réflexion sur le passage des voisins construits pour le DBSCA ...
