import numpy as np
import graph_carre as gc
import time as t
import random as rd
import matplotlib.pyplot as plt
import clustering as clu

def nouveau_grain(grain,ch_max,nb,alpha):
    """Permet un calcul plus fin du grain lors des appels récusif du dbsca = floor((nb/ch_max)^alpha)
    nb = nb courant dans le cluster que l'on va réduire
    alpha = puissance
    ch_max = nombre max de
    (!) un grain de 1 ne doit jamais rentrer dans la fct !"""
    #A n'utiliser que si le grain est supérieur à 1
    new = int(np.floor(grain/(np.power(nb/ch_max,alpha))))
    if (new == grain):
        return (new - 1)
    else:
        return (new)


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

def creer_tab_voisins(g,commandes): #0(n^2*ln(n)) avec n = nb commandes
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

def DBSCA(graph,commandes,nb_max_elt,grain_depart, voisins,alpha): #fonction récursive
    """fait les groupes de livraison pour les commandes avec des groupes d'au plus nb_max_elt à partir de la liste de commandes, de graph, et d'un grain de départ
    grain toujours entier"""
    #ne relancer que sur les groupes de trop grande taille
    #que contient commande ?
    liste_clust,to_check,v_new = DBSCA_classique(graph,commandes,nb_max_elt,grain_depart,voisins)
    if len(to_check) == 0:
        return liste_clust
    else:
        for elt in to_check:
            nb = len(elt)
            grain = nouveau_grain(grain_depart,nb_max_elt,nb,alpha)
            liste_finale = DBSCA(graph,elt,nb_max_elt,grain,v_new,alpha) #tant que les groupes sont trop grands, on relance le dbsca dessus de manière récursive
            liste_clust.extend(liste_finale)
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

def parcours_resto(graph,commandes,nb_livreurs,charge_max,alpha): #n^2ln(n) - DBSCA
    """entree : liste de commandes, nb de livreurs, charge max en un parcours
sortie dictionnaire - clé numéro de livreur - liste de trajets à effectuer -[position resto - à visiter 1--- à visiter (n-1) - position resto]"""

    #etape0 = generer la liste des voisins
    voisins = creer_tab_voisins(graph,commandes)

    #etape1 = faire les clusters - heuristique de démarrage à préciser et à affiner
    side = graph.get_side_l()
    nb_commandes = len(commandes)

    #grain de départ = côté * Chmax /(nb_Livreurs * nb_Commandes)
    grain_depart = side
    cluster = DBSCA(graph,commandes,charge_max,grain_depart,voisins,alpha)
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

"""size_city = 100
nb_commandes = 20
g = gc.graph_carre(size_city)
cmds = gc.commandes_tab(g,nb_commandes)
g.set_restaurant((size_city)//2,(size_city)//2)
nb_liv = 3
charge_max = 4
alpha = 0.1
#print("alpha\n",parcours_resto(g,cmds,nb_liv,charge_max,alpha))"""

"""
def testfor_alpha(nb_livreurs,capacity,size_city,resto,nb_commandes,alpha):
    #permet de lancer une simulation de livraison avec le alpha en paramètre et de récupérer le temps moyen
    g = gc.graph_carre(size_city)
    g.set_restaurant(resto[0],resto[1])

    cmds = gc.commandes_tab(g,nb_commandes)

    dico = parcours_resto(g,cmds,nb_livreurs,capacity,alpha) #lancement de la simulation
    tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,9)
    return time_avg
"""

def tab_graph_construction_alphatest(size_city,charge_max,nb_commandes,nb_livreurs,alpha_min, alpha_max,ok,nb_echantillons,count_max):
    """construit les deux tableaux nécessaires à la construction du paramètre alpha optimal - dichotmie accéléré
    -alpha_min, alpha_max : paramètres alpha avec lequels on commence (alpha_min < alpha_max)
    -ok = ecart entre la moyenne precedente et la nouvelle moyenne considéré comme acceptable = condition d'arrêt
    - count_max = nombre maximum de tentatives de alpha possibles"""
    xfinal = [i for i in range(1,(nb_echantillons + 1))] #axe x pour le plt.plot
    yfinal = []
    yerrfinal = []
    non_valid = True #tant que le ok n'a pas été vérifié
    count = 0 #affichage qui permet de suivre où on en est dans les tests
    alpha_stock = [0,alpha_min] #tableau de stockage des valeurs de alpha testés - 0 pour le cas sans alpha
    situations = [] #liste de commandes pour tous
    g = gc.graph_carre(size_city)
    g.set_restaurant((size_city)//2,(size_city)//2)
    time_mean = []
    timing = []

    alpha_old = alpha_min #le alpha qui aura déjà été calculé
    alpha_new = alpha_max #celui qui sera calculé dans la boucle
    y = []
    yerr = []
    temps = []
    """
    for i in range(nb_echantillons): #boucle avant entrée dans la récursion - même chose que la boucle interne
        print("boucle",count,i)
        temps.append(testfor_alpha(nb_livreurs,charge_max,size_city, (size_city//2,size_city//2),nb_commandes,alpha_old))
        temps_np = np.array(temps)
        avg = np.mean(temps_np)
        incertitude = np.std(temps_np)/np.sqrt(i+1)
        y.append(avg)
        yerr.append(incertitude)
    """
    for i in range(nb_echantillons): #initialisation des commandes possibles - pour que tout le monde soit testé sur les mêmes situations de commandes
        situations.append(gc.commandes_tab(g,nb_commandes))

    #print(situations)
    for i in range(nb_echantillons): #on prend en compte les essais précédents pour voir la convergence dans une même situation-boucle à vide sans le alpha (clustering originel)
        print("initialisation - sans alpha",i)
        ti = t.time()
        dico = clu.parcours_resto(g,situations[i],nb_livreurs,charge_max) #lancement de la simulation
        timing.append(t.time()-ti)
        tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,30) #récupérations résultats de la simulation - longeur et vitesse

        temps.append(time_avg) #temps moyen qu'il a fallu pour livrer les commandes
        temps_np = np.array(temps)
        avg = np.mean(temps_np)
        incertitude = np.std(temps_np)/np.sqrt(i+1)
        y.append(avg)
        yerr.append(incertitude)

    time_mean.append(np.mean(timing))
    yfinal.append(y)
    yerrfinal.append(yerr)

    #réinitialisation des variables pour le calcul suivant
    y = []
    yerr = []
    temps = []
    timing = []

    for i in range(nb_echantillons): #on prend en compte les essais précédents pour voir la convergence dans une même situation
        print(f"alpha {alpha_old} boucle {count} {i}")
        ti = t.time()
        dico = parcours_resto(g,situations[i],nb_livreurs,charge_max,alpha_old) #lancement de la simulation
        timing.append(t.time() - ti)
        tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,30) #récupérations résultats de la simulation - longeur et vitesse

        temps.append(time_avg)
        temps_np = np.array(temps)
        avg = np.mean(temps_np)
        incertitude = np.std(temps_np)/np.sqrt(i+1)
        y.append(avg)
        yerr.append(incertitude)

    time_mean.append(np.mean(timing))
    yfinal.append(y)
    yerrfinal.append(yerr)
    avg_old = y[nb_echantillons-1] #dernière moyenne = vrai temps moyen au bout de tout les essais

    while non_valid: #tant que le critère ok n'a pas été respecté
        count += 1
        y = []
        yerr = []
        temps = []
        timing = []
        print("temps",temps)
        print(alpha_new,alpha_old)


        for i in range(nb_echantillons): #on prend en compte les essais précédents pour voir la convergence dans une même situation
            print(f"alpha {alpha_new} boucle {count} {i}")
            ti = t.time()
            dico = parcours_resto(g,situations[i],nb_livreurs,charge_max,alpha_new) #lancement de la simulation
            timing.append(t.time() - ti)
            tmps_pr_maison,time_avg = gc.time_to_deliver(g,dico,100,30) #récupérations résultats de la simulation - longeur et vitesse

            temps.append(time_avg)
            temps_np = np.array(temps)
            avg = np.mean(temps_np)
            incertitude = np.std(temps_np)/np.sqrt(i+1)
            y.append(avg)
            yerr.append(incertitude)

        avg_new = y[nb_echantillons-1] #nouvelle moyenne obtenue - à comparer
        yfinal.append(y)
        yerrfinal.append(yerr)
        alpha_stock.append(alpha_new)
        time_mean.append(np.mean(timing))

        print("avg diff :",(avg_new-avg_old))

        if ((abs(avg_new - avg_old))<= ok) or (count >= count_max):#si l'écart entre les deux est inférieur à ok, on  renvoie le plus petit des deux
            non_valid = False
            if avg_new < avg_old : #on renvoie le meilleur alpha sur les deux
                return alpha_new, alpha_stock, xfinal, yfinal, yerrfinal, time_mean
            else:
                return alpha_old, alpha_stock, xfinal, yfinal, yerrfinal, time_mean
        else:
            alpha_s = alpha_new
            alpha_new = (alpha_new + alpha_old)/2 #nouvel alpha à tester
            if avg_new < avg_old: #si le nouveau résultat est meilleur = ON LE CONSERVE
                avg_old = avg_new
                alpha_old = alpha_s
            #sinon on ne fait rien (avg_new va être effacé)

alpha_final, alpha_stock, xfinal, yfinal, yerrfinal, time_mean = tab_graph_construction_alphatest(100,10,20,3,0.001,1,5.0,300,20)
#size_city,charge_max,nb_commandes,nb_livreurs,alpha_min, alpha_max,ok,nb_echantillons,count_max
print(time_mean)

plt.plot(xfinal,yfinal[i],'-',label=f"sans alpha - essai {0}")
for i in range(1,len(yfinal)):
    plt.plot(xfinal,yfinal[i],'-',label=f"alpha : {alpha_stock[i]} essai {i}")

plt.legend()

plt.show()

plt.plot(alpha_stock[1:],time_mean[1:],'rx',label="alphas")
plt.plot([1.5],[time_mean[0]],'bx',label="original")
plt.legend()
plt.show()