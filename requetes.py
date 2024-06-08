
import json
import networkx as nx
import matplotlib.pyplot as plt
import time 

def txt_json(fichier):
    """Convertit les données d'un fichier texte au format JSON.

    Paramètres:
        fichier (str): Le chemin vers le fichier texte.

    Complexité: O(n*m), où n est le nombre de lignes dans le fichier et m est le nombre de caractères dans chaque ligne.
    """
    fic = open(fichier, 'r', encoding='utf8')
    fic_json = open("data/data.json", 'w', encoding='utf8')
    lignes = fic.readlines()
    films = []
    for ligne in lignes:
        data = json.loads(ligne)
        modif = {}
        liste = []
        for titre, valeur in data.items():
            if type(valeur) == list:
                for carac in valeur:
                    carac = carac.strip('"').replace("[[", "")
                    carac = carac.strip('"').replace("]]", "")
                    liste.append(carac)
                modif["collaborateurs"] = liste
            if type(valeur) == str:
                modif[titre] = valeur
        films.append(modif)
    with open("data/data.json", "w", encoding='utf8') as f:
        json.dump(films, f, indent=4, ensure_ascii=False)


def json_vers_nx(chemin):
    """Convertit les données JSON en un graphe NetworkX.

    Paramètres:
        chemin (str): Le chemin vers le fichier JSON.

    Retourne:
        networkx.Graph: Le graphe NetworkX représentant les données de collaboration.

    Complexité: O(n*m), où n est le nombre de films et m est le nombre de collaborateurs dans chaque film.
    """
    G = nx.Graph()
    with open(chemin, "r",encoding='utf-8') as f:
        data = json.load(f)
        for film in data:
            acteurs = film.get("collaborateurs", [])
            for i in range(len(acteurs)):
                for j in range(i+1, len(acteurs)):
                    G.add_edge(acteurs[i], acteurs[j])
    return G


def collaborateurs_communs(acteurs1, acteurs2):
    """Trouve les collaborateurs communs entre deux acteurs/actrices.

    Paramètres:
        acteurs1 (str): Nom du premier acteur/actrice.
        acteurs2 (str): Nom du deuxième acteur/actrice.

    Retourne:
        set: Ensemble de collaborateurs communs.

    Complexité: O(n), où n est le nombre de films.
    """
    with open("data/data.json", "r") as f:
        data = json.load(f)
    ens = set()
    for film in data:
        acteurs = film.get("collaborateurs", [])
        if acteurs1 in acteurs and acteurs2 in acteurs:
            ens.update(acteurs)
    ens.discard(acteurs1)
    ens.discard(acteurs2)
    return ens


def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un ilustre inconnu.")
        return None
    collaborateurs = set()
    collaborateurs.add(u)

    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs: 
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs



def est_proche(G, u, v,k=1):
    """Fonction renvoyant True si u et v sont reliés dans le graphe G, False sinon.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet
    """
    
    if u not in collaborateurs_proches(G,v,k):
        return False
    return True

#print(est_proche(G,"John Cazale","Harrison Ford"))



def distance_naive(G, u, v):
    """ Fonction renvoyant la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet de départ, un acteur
        v (String): le sommet d'arrivée, un acteur

    Returns:
        int: la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Complexité: O(n+e) où n est le nombre de sommets et e le nombre d'arêtes du graphe.
    """
    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    
    collaborateurs = set()
    collaborateurs.add(u)
    n = 1  # Initialisation de la distance à 1
    
    while collaborateurs: # Boucle tant qu'il y a des collaborateurs à examiner
        collaborateurs_directs = set() # Ensemble pour stocker les collaborateurs directs au prochain niveau
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin == v: # Si le voisin est v, retourne la distance actuelle
                    return n 
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin) # Si le voisin n'est pas déjà un collaborateur, l'ajoute à l'ensemble des collaborateurs directs
        
        if not collaborateurs_directs:    # Si aucun nouveau collaborateur n'est trouvé, v n'est pas accessible depuis u
            return None
        collaborateurs = collaborateurs_directs # Met à jour les collaborateurs pour le prochain niveau de recherche
        n += 1
    
    return None


def distance(G,u,v):
    """Fonction renvoyant la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet

    Complexité: O(n+e) où n est le nombre de sommets et E le nombre d'arêtes du graphe.
    """

    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    try:

        return nx.shortest_path_length(G,u,v) # Utilisation de la fonction de NetworkX pour calculer la distance
    
    except nx.NetworkXNoPath: # Si aucun chemin n'existe entre u et v

        return None


def pre_calcul(G):
    """Pré-calculer les distances entre toutes les paires de sommets en utilisant l'algorithme de Floyd-Warshall sans utiliser l'infini.
    
    Complexité: O(n^3), où n est le nombre de sommets.
    
    Paramètres:
        G: NetworkX Graph, le graphe des collaborations
    
    Retourne:
        dist_matrix: dict, un dictionnaire de dictionnaires représentant la matrice des distances
    """
    # Initialiser la matrice des distances
    dist_matrix = {}
    for node in G.nodes:
        dist_matrix[node] = {}
        for node2 in G.nodes:
            dist_matrix[node][node2] = None
    
    # La distance de chaque sommet à lui-même est 0
    for node in G.nodes:
        dist_matrix[node][node] = 0
        
    # La distance entre deux sommets directement connectés est l'arête entre eux (1 pour des graphes non pondérés)
    for u, v in G.edges():
        dist_matrix[u][v] = 1
        dist_matrix[v][u] = 1
    
    # Application de l'algorithme de Floyd-Warshall pour calculer les distances
    for k in G.nodes:
        for i in G.nodes:
            for j in G.nodes:
                if dist_matrix[i][k] is not None and dist_matrix[k][j] is not None:
                    if dist_matrix[i][j] is None or dist_matrix[i][j] > dist_matrix[i][k] + dist_matrix[k][j]:
                        dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
    return dist_matrix

def distance_pre_calcul(dist_matrix, u, v):
    """Récupérer la distance entre deux sommets à partir de la matrice pré-calculée.
    
    Complexité: O(1)
    
    Paramètres:
        dist_matrix: dict, la matrice des distances pré-calculées
        u: str, un sommet du graphe
        v: str, un autre sommet du graphe
    
    Retourne:
        distance: int ou None, la distance entre u et v, ou None si aucun chemin n'existe
    """
    return dist_matrix[u][v] if u in dist_matrix and v in dist_matrix[u] else None


def centralite(G, u):
    """Fonction renvoyant la centralité de l'acteur u dans le graphe G par rapport à la plus grande distance qui le sépare d'un autre acteur. La fonction renvoie None si u est absent du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet, un acteur

    Returns:
        int: la centralité de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.

    Complexité: O(n+e) où N est le nombre de sommets et E le nombre d'arêtes du graphe.

    """
    if u not in G.nodes:
        print(u, "est absent du graphe.")
        return None
    
    dico = {u : 0}
    a_traiter = [u]
    while a_traiter:
        sommet = a_traiter.pop(0)
        for voisin in G.adj[sommet]:
            if voisin not in dico:
                dico[voisin] = dico[sommet] + 1
                a_traiter.append(voisin)
    
    return max(dico.values())

def centralite_pre_calcul(G,u):
    """Calcul de la centralité de proximité en utilisant la matrice des distances pré-calculée.

    Args:
        G (networkx.Graph): Le graphe

    Returns:
        dict: Un dictionnaire contenant les centralités de proximité de chaque acteur

    Complexité:
        O(n^3) :  ou n est le nombre de sommets du graphe.
    """
    dist_matrix = pre_calcul(G)  # Pré-calcul de la matrice des distances
    centralites = {}  # Dictionnaire pour stocker les centralités de proximité de chaque acteur

    # Calcul de la centralité de proximité pour chaque acteur
    for acteur in G.nodes:
        # Compteur pour calculer la somme des distances de cet acteur à tous les autres acteurs
        somme_distances = 0
        
        # Calcul de la somme des distances de cet acteur à tous les autres acteurs
        for autre_acteur in G.nodes:
            if acteur != autre_acteur:  # Exclure l'acteur lui-même
                distance = dist_matrix[acteur][autre_acteur]
                if distance is not None:
                    somme_distances += distance
        
        # Calcul de la centralité de proximité pour cet acteur
        if somme_distances == 0:
            centralite = 1  # Si l'acteur est isolé, sa centralité est définie comme 0
        else :
            centralite = 1 // somme_distances
        # Ajout de la centralité de proximité au dictionnaire
        centralites[acteur] = centralite+1
    return centralites[u]

    
def centre_holywood(G):
    """Fonction renvoyant l'acteur le plus central du graphe G par rapport au minimum de centralite par acteur .
    
    Parametres:
        G: le graphe
    Returns:
        str: l'acteur le plus central du graphe G
    Complexité: O(N^2+NE) où N est le nombre de sommets et E le nombre d'arêtes du graphe.
    """

    centralites = {acteur: centralite(G,acteur) for acteur in G.nodes}
    centre = min(centralites, key=centralites.get)
    return centre




def eloignement_max(G):
    """Fonction renvoyant la distance maximale entre deux acteurs du graphe G .
    Parametres:
        G: le graphe
    Returns:
        int: la distance maximale entre deux acteurs du graphe G

    Complexité: O(N^2+ N*E) où N est le nombre de sommets et E le nombre d'arêtes du graphe.
    """
    max_distance = 0
    cpt = 0
    for acteur in G.nodes:
        print(cpt)
        cpt+=1
        c = centralite(G, acteur)
        if c is not None and c > max_distance:
            max_distance = c


    return max_distance


#Bonus
def centralite_groupe(G, s):
    centralities = {actor: centralite(G, actor) for actor in s}
    center_actor = min(centralities, key=centralities.get)
    return center_actor


def collaborateurs_proches2(G,u,k):
    proches = collaborateurs_proches(G,u,k)
    SG = G.subgraph(proches)
    plt.clf()
    nx.draw(SG, with_labels=True)
    plt.show()
    return SG

    
    

#collaborateurs_proches2(G,"Harrison Ford",1)