import graph_carre as gc

def creer_tab_voisins(g,commandes):
    """Crée un dictionnaire à partir des sommets à visiter, les clés sont les sommets de la liste de commandes, 
    et les valeurs associée sont une liste des autres sommets à visiter, par ordre croissant de distance au sommet courant"""
    tabvoisins = {}

    for u in commandes:
        tabvoisins[u] = []
        for v in commandes:
            if v != u:
                tabvoisins[u].append((v,gc.dist(g,u,v)))
    for w in commandes:
        tabvoisins[w] = sorted(tabvoisins[w],key = lambda pt: pt[1])

    return tabvoisins


def créer_grp(commandes,tab_v,siz = 3):
    """crée des groupes de 3 sommets (ou moins si aucun sommet ne reste) qui seront attribués à différents livreurs"""
    G = []
    return G





g = gc.graph_carre(10)
g.set_restaurant(3,6)
gc.verify(g,gc.test(g))

cmds = gc.commandes_tab(g,17)
print(creer_tab_voisins(g,cmds))

