import clustering as cl

def extract(commandes,repartition,group):
    """extrait les maisons de la liste de commandes du groupe k"""
    out = []
    for ind in range(len(commandes)):
        if (repartition[ind] == group):
            out.append(commandes[ind])
    return out

def solving_out(repartition,commandes,nb_elts,nb_groups,nb_max,graph,voisins):
    value_out = 0
    for k in range(nb_groups): #pour chaque groupe = chaque livreur on calcule le coût du parcours
        to_solve = extract(commandes,repartition,k)
        #print("to_solve",to_solve)
        new_nb_elts = len(to_solve) #extrait les maisons de la liste de commandes du groupe k
        if (new_nb_elts > nb_max): #si le cardinal par livreur est trop grand
            #print("toobig")
            new_nb_groups = new_nb_elts//nb_max
            if (new_nb_elts%nb_max != 0): #pour si jamais cela ne tombe pas exactement pile
                new_nb_groups += 1

            value_out += group_generation(new_nb_elts,new_nb_groups,to_solve,nb_max,nb_max,graph,voisins,"tour 2") #on relance une rerépartition en groupes
        elif (new_nb_elts > 0):
            #print("okay size")
            start = graph.get_resto()
            parc,dist = cl.tree_cuting(graph,to_solve,start,voisins)
            value_out += dist
    #print("current value_out",value_out)
    return value_out



def check_worth_relance(tab,value,ind_max,nb_max):
    """renvoie True si dans le tableau tab des indices 0 à ind_max il y a nb_max ou moins fois la valeur value"""
    ind = 0
    count = 0
    while (ind < ind_max):
        if (tab[ind] == value):
            count+=1
        if (count == nb_max): #n'ayant pas encore atteint le dernier objet, on sait qu'il y en a un de trop
            return False
        ind += 1
    return True

def group_generation(nb_elts,nb_groups,commandes,nb_max_current,nb_max_real,graph,voisins,label): #voisins non filtré (filtrage effectué dans tree_cutting)

    def rec_gp(ind,out,nb_elts,nb_groups,commandes,nb_max_current,nb_max_real,graph,voisins,label):
        """génère toutes les répartitions dans nb_groups de nb_elts"""
        if (ind == nb_elts):
            #print(out)
            #return out[ind//2] + out[ind//4]
            return solving_out(out,commandes,nb_elts,nb_groups,nb_max_real,graph,voisins) #renvoie le temps de livraison minimal dans cette disposition
        else:
            min = 1e15
            a = 1e15
            for k in range(nb_groups):
                out[ind] = k
                if check_worth_relance(out,k,ind,nb_max_current):
                    #print("here")
                    a = rec_gp((ind + 1),out,nb_elts,nb_groups,commandes,nb_max_current,nb_max_real,graph,voisins,label)
                if (a < min):
                    #print("minima")
                    min = a
            #print("min",label,min)
            return min

    return rec_gp(0,[0 for _ in range(nb_elts)],nb_elts,nb_groups,commandes,nb_max_current,nb_max_real,graph,voisins,label)

#group_generation(6,4,[],3)

def situation_test_bruteforce(graph,commandes,nb_livreurs,charge_max_livreurs):
    voisins = cl.creer_tab_voisins(graph,commandes)

    nb_commandes = len(commandes)
    if (nb_commandes%(nb_livreurs*charge_max_livreurs) == 0): #pour si jamais cela ne tombe pas exactement pile
        taille_max_groupe = nb_commandes//nb_livreurs
    else:
        taille_max_groupe = charge_max_livreurs*((nb_commandes//(nb_livreurs*charge_max_livreurs)) + 1)

    #print(taille_max_groupe)
    return group_generation(nb_commandes,nb_livreurs,commandes,taille_max_groupe,charge_max_livreurs,graph,voisins,"tour 1")
    #nécessaire de bien calibrer en combien de groupes on réparti les elts car ce nombre doit être dans certains cas supérieur au nombre de livreurs

def calcul_dist_parcours(parcours,graph):
    """calcule la distance parcourue par tout les livreurs via un parcours calculé selon notre algorithme (ici parcours_resto)"""
    out = 0
    for key in parcours.keys():
        for cl in range(len(parcours[key])):
            for ind in range(len(parcours[key][cl]) - 1):
                out += gc.dist(graph,parcours[key][cl][ind],parcours[key][cl][ind + 1])
    return out


def brute_force_comparaison(nb_essais,size_city,resto,nb_commandes,nb_livreurs,charge_max):
    ecart = []
    brutforce = []
    dbsca = []
    ratio = []

    for i in range(nb_essais):
        print(i)
        g = gc.graph_carre(size_city)
        g.set_restaurant(resto[0],resto[1])

        cmds = gc.commandes_tab(g,nb_commandes)
        distb =  situation_test_bruteforce(g,cmds,nb_livreurs,charge_max)
        para = cl.parcours_resto(g,cmds,nb_livreurs,charge_max)
        #print(para)
        dista = calcul_dist_parcours(para,g)

        brutforce.append(distb)
        dbsca.append(dista)
        ecart.append(dista - distb)
        ratio.append(dista/distb)

    return brutforce, dbsca, ecart, ratio


def test6(size_city,resto,nb_commandes,nb_livreurs,charge_max_livreurs):
    g = gc.graph_carre(size_city)
    g.set_restaurant(resto[0],resto[1])

    cmds = gc.commandes_tab(g,nb_commandes)
    print(cmds)
    print("result",situation_test_bruteforce(g,cmds,nb_livreurs,charge_max_livreurs))

    if (nb_commandes%(nb_livreurs*charge_max_livreurs) == 0): #pour si jamais cela ne tombe pas exactement pile
        taille_max_groupe = nb_commandes//nb_livreurs
    else:
        taille_max_groupe = charge_max_livreurs*((nb_commandes//(nb_livreurs*charge_max_livreurs)) + 1)

    print(taille_max_groupe)

#test6(100,(50,50),8,2,3)
def test_brute_force():
    brut,dbsca, ecart, ratio = brute_force_comparaison(10,100,(50,50),9,2,3)
    print("résultat bruteforce",brut)
    print("résultat notre algo",dbsca)
    print("résultat ecart",ecart)
    print("résultat quotient des resultats",ratio)

test_brute_force()

def length_sorted(tab):
    support = []
    for ind in range(len(tab)):
        support.append((tab[ind],len(tab[ind])))
    print(support)
    support = sorted(support,reverse = True,key = lambda pt: pt[1])
    for ind in range(len(tab)):
        tab[ind] = support[ind][0]
