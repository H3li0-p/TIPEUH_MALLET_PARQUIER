# TIPEUH
Lycée Michel Montaigne, MP2I 2024-2025 TIPE

Référents :

M Sartre : LaurentSartre;
Mme Olivier : geraldineolivier

(Idées en vrac)
Algo plus court chemin
Utiliser matrices d'adjacence

(A^n) donne le nombre de chemins de longueur entre i,j
Bref
Utiliser une matrice « associée » -> matrice de bool
(1 si chemin,0 sinon) pour les calculs
L’associer à une implémentation donnant la liste des voisins ?
Le but est de donner le plus court chemin

Situation à modéliser : un resto qui a un service de livraison de pâtes (pas fonda pâtes mais c'est rigolo), et qui doit livrer des maisons à différentes adresses. Le but est d'optimiser le rendement nombre de livreurs / temps d'attente des clients et de trouver un algo pour optimiser le temps de parcours des livreurs.
On veut modéliser la situation avec des graphes

Echelle 1 :
1 resto
1 livreur - vont toujours à la même vitesse
prise en compte de la distance entre les lieux

Echelle 2 :
1 resto
possiblement plusieurs livreurs - vont toujours à la même vitesse
prise en compte de la distance entre les lieux

Echelle 3 :
1 resto
possiblement plusieurs livreurs
prise en compte de la distance entre les lieux - apparition de limites de vitesses (peut être de notion de flux ?)

Echelle 4 :
1 resto
possiblement plusieurs livreurs
prise en compte de la distance entre les lieux - apparition de limites de vitesses / flux et densité de la route / probabilité d'aléas (feu rouge, accident ...)
temps de préparation des plats

Echelle 5:
plusieurs resto
possiblement plusieurs livreurs
ce qu'on va réussir à adapter des modèles

Temps d'acceptabilité pour une commande : 30 min = 0.5 h
Salaire moyen d'un livreur :
