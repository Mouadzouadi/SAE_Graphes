
import json
import networkx as nx
import matplotlib.pyplot as plt
import time 

import requetes as sae

def txt_jsonTemps(fichier):
    debut = time.time()
    fic = open(fichier, 'r',encoding='utf8')
    fic_json = open("data/data.json",'w')
    lignes = fic.readlines()
    films = []
    for ligne in lignes:
        data = json.loads(ligne)
        modif = {}
        liste = []
        for titre, valeur in data.items():
            if type(valeur) == list :
                for carac in valeur:
                    carac = carac.strip('"').replace("[[", "")
                    carac =carac.strip('"').replace("]]", "")
                    liste.append(carac)
                modif["collaborateurs"] = liste
            if type(valeur) == str:
                modif[titre] = valeur
        films.append(modif)
    with open("data/data.json", "w", encoding='utf8') as f:
        json.dump(films,f,indent=4,ensure_ascii=False)
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_txt_json(n):
    res = 0
    for i in range(n):
        res += txt_jsonTemps("data/data.txt")
    return res/n
#print("Temps d'execution moyen de txt_json",temps_moy_txt_json(100),"s")

def json_vers_nxTemps(chemin):
    debut = time.time()
    G = nx.Graph()
    with open(chemin, "r", encoding='utf8') as f:
        data = json.load(f)
        for film in data:
            acteurs = film.get("collaborateurs", [])
            for i in range(len(acteurs)):
                for j in range(i+1, len(acteurs)):
                    G.add_edge(acteurs[i], acteurs[j])
    fin = time.time()
    return round(fin-debut,5)


def temps_moy_json_nx(n):
    res = 0
    for i in range(n):
        res += json_vers_nxTemps("data/data.txt")
    return res/n
#print("Temps d'execution de json_vers_nx",temps_moy_json_nx("data/data.json"),"s")

def collaborateurs_communsTemps(acteurs1, acteurs2):
    debut = time.time()
    
    # Charger les données JSON
    with open("data/data.json", "r") as f:
        data = json.load(f)
    
    # Initialiser un ensemble pour les collaborateurs communs
    ens = set()
    
    # Parcourir les films pour trouver les collaborations
    for film in data:
        acteurs = film.get("collaborateurs", [])
        if acteurs1 in acteurs and acteurs2 in acteurs:
            ens.update(acteurs)
    
    # Retirer les acteurs de la recherche (acteurs1 et acteurs2)
    ens.discard(acteurs1)
    ens.discard(acteurs2)
    fin = time.time()
    
    
    return round(fin-debut,5)

def temps_moy_collaborateurs(n):
    txt_jsonTemps("data/data_1000.txt")  
    G = sae.json_vers_nx("data/data.json")
    res = 0
    for i in range(n):
        res+= collaborateurs_communsTemps("Ben Affleck", "Henry Cavill")
    return res/n
#print("Temps d'execution moyen de collaborateurs commun",temps_moy_collaborateurs(100),"s") 

def collaborateurs_prochesTemps(G, u, k):
    debut = time.time()
    if u not in G.nodes:
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
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_collaborateurs_proches(n):
    res = 0
    txt_jsonTemps("data/data_1000.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += collaborateurs_prochesTemps(G, "Ben Affleck", 2)
    return res/n

#print("Temps d'execution moyen de collaborateurs proches:", temps_moy_collaborateurs_proches(100), "s")


def est_procheTemps(G, u, v, k=1):
    debut = time.time()
    res = u in collaborateurs_prochesTemps(G, v, k)
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_est_proche(n):
    res = 0
    txt_jsonTemps("data/data_100.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += est_procheTemps(G, "John Cazale", "Harrison Ford", 2)
    return res/n

#print("Temps d'execution moyen de est proche:", temps_moy_est_proche(100), "s")
 #Test des distances
def distance_naiveTemps(G, u, v):
    debut = time.time()
    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    
    collaborateurs = set()
    collaborateurs.add(u)
    n = 1
    
    while collaborateurs:
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin == v:
                    fin = time.time()
                    return round(fin-debut,5)
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        
        if not collaborateurs_directs:
            return None
        collaborateurs = collaborateurs_directs
        n += 1
    
    fin = time.time()
    return fin-debut

def temps_moy_distance_naive(n):
    res = 0
    txt_jsonTemps("data/data_2.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += distance_naiveTemps(G, "Harrison Ford", "John Cazale")
    moyenne = (res/len(G.nodes))/n
    moyenne_str = "{:.9f}".format(moyenne)
    return moyenne_str

#print("Temps d'execution moyen de distance naive:", temps_moy_distance_naive(1000), "s")

def distanceTemps(G, u, v):
    debut = time.time()
    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    try:
        nx.shortest_path_length(G, u, v)
    except nx.NetworkXNoPath:
        pass
    fin = time.time()
    return fin-debut

def temps_moy_distance(n):
    res = 0
    txt_jsonTemps("data/data_2.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += distanceTemps(G, "Harrison Ford", "John Cazale")
    moyenne = (res/len(G.nodes))/n
    moyenne_str = "{:.9f}".format(moyenne)
    return moyenne_str

#print("Temps d'execution moyen de distance:", temps_moy_distance(1000), "s")

def pre_calcul(G):
    """Pré-calculer les distances entre toutes les paires de sommets en utilisant l'algorithme de Floyd-Warshall sans utiliser l'infini.
    
    Complexité: O(n^3), où n est le nombre de sommets.
    
    Paramètres:
        G: NetworkX Graph, le graphe des collaborations
    
    Retourne:
        dist_matrix: dict, un dictionnaire de dictionnaires représentant la matrice des distances
    """
    # Initialiser la matrice des distances
    debut = time.time() 
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
                       
    fin = time.time()
    return dist_matrix, round(fin-debut,5)

def distance_pre_calcul_Temps(dist_matrix, u, v):
    """Récupérer la distance entre deux sommets à partir de la matrice pré-calculée.
    
    Complexité: O(1)
    
    Paramètres:
        dist_matrix: dict, la matrice des distances pré-calculées
        u: str, un sommet du graphe
        v: str, un autre sommet du graphe
    
    Retourne:
        distance: int ou None, la distance entre u et v, ou None si aucun chemin n'existe
    """
    temps2 = time.time()
    temps1 = dist_matrix[1]
    if u in dist_matrix[0] and v in dist_matrix[0][u]:
        fin = time.time()
        return round((fin-temps2)+temps1,5)
    else:
        fin = time.time()
        return round((fin-temps2)+temps1,5)
    

def temps_moy_pre_calcul(n):
    res = 0
    txt_jsonTemps("data/data_2.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += distance_pre_calcul_Temps(pre_calcul(G), "Harrison Ford", "John Cazale")
    moyenne = (res/len(G.nodes))/n
    moyenne_str = "{:.9f}".format(moyenne)
    return moyenne_str

#print("Temps d'execution moyen de pre-calcul:", temps_moy_pre_calcul(1000), "s")


def centralite_dis_temps(G, u):
    """Fonction renvoyant la centralité de l'acteur u dans le graphe G par rapport à la plus grande distance qui le sépare d'un autre acteur. La fonction renvoie None si u est absent du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet, un acteur

    Returns:
        int: la centralité de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.

    Complexité: O(N(N+E)) où N est le nombre de sommets et E le nombre d'arêtes du graphe.

    """
    debut = time.time()
    if u not in G.nodes:
        return None
    centralite = 0
    for voisin in G.nodes:
        if voisin != u:
            d = sae.distance(G,u,voisin)
            if d is not None and d > centralite:
                centralite = d
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_centralite_dis(n):
    res = 0
    txt_jsonTemps("data/data_2.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += centralite_dis_temps(G,"Harrison Ford")
    return res/n
#print("Temps d'execution moyen de centralite_dis:", temps_moy_centralite_dis(1000), "s")
def centralite_pre_calcul(G,u):
    """Calcul de la centralité de proximité en utilisant la matrice des distances pré-calculée.

    Args:
        G (networkx.Graph): Le graphe

    Returns:
        dict: Un dictionnaire contenant les centralités de proximité de chaque acteur

    Complexité:
        O(n^3) ou n est le nombres de sommets du graphe .
    """
    debut = time.time()
    dist_matrix = pre_calcul(G)  # Pré-calcul de la matrice des distances
    centralites = {}  # Dictionnaire pour stocker les centralités de proximité de chaque acteur

    # Calcul de la centralité de proximité pour chaque acteur
    for acteur in G.nodes:
        # Compteur pour calculer la somme des distances de cet acteur à tous les autres acteurs
        somme_distances = 0
        
        # Calcul de la somme des distances de cet acteur à tous les autres acteurs
        for autre_acteur in G.nodes:
            if acteur != autre_acteur and acteur is not None and autre_acteur is not None :  # Exclure l'acteur lui-même
                distance = dist_matrix[0][acteur][autre_acteur]
                if distance is not None:
                    somme_distances += distance
        
        # Calcul de la centralité de proximité pour cet acteur
        if somme_distances != 0:
            centralite = 1 / somme_distances
        else:
            centralite = 0  # Si l'acteur est isolé, sa centralité est définie comme 0
        
        # Ajout de la centralité de proximité au dictionnaire
        centralites[acteur] = centralite
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_centralite_pre_calcul(n):
    res = 0
    txt_jsonTemps("data/data_2.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += centralite_pre_calcul(G,"Harrison Ford")
    return res/n
#print("Temps d'execution moyen de centralite_pre_calcul:", temps_moy_centralite_pre_calcul(1000), "s")

def centralite_Temps(G, u):
    """Fonction renvoyant la centralité de l'acteur u dans le graphe G par rapport à la plus grande distance qui le sépare d'un autre acteur. La fonction renvoie None si u est absent du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet, un acteur

    Returns:
        int: la centralité de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.

    Complexité: O(N(N+E)) où N est le nombre de sommets et E le nombre d'arêtes du graphe.

    """
    debut = time.time()
    if u not in G.nodes:
        return None
    centralite = 0
    for voisin in G.nodes:
        if voisin != u:
            d = sae.distance(G,u,voisin)
            if d is not None and d > centralite:
                centralite = d
    fin = time.time()
    return round(fin-debut,2)

def temps_moy_centralite(n):
    res = 0
    txt_jsonTemps("data/data_1000.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += centralite_Temps(G, "Harrison Ford")
    
    moyenne = (res/len(G.nodes))/n
    moyenne_str = "{:.5f}".format(moyenne)
    return moyenne_str
#print("Temps d'execution moyen de centralite:", temps_moy_centralite(100), "s")

def centre_holywoodTemps(G):
    debut = time.time()
    centralites = {acteur: sae.centralite(G,acteur) for acteur in G.nodes}
    centre = min(centralites, key=centralites.get)
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_centre_holywood(n):
    res = 0
    txt_jsonTemps("data/data.txt")  
    G = sae.json_vers_nx("data/data.json")
    for i in range(n):
        res += centre_holywoodTemps(G)
    return res/n

#print("Temps d'execution moyen de centre_holywood:", temps_moy_centre_holywood(1), "s")


def eloignement_maxTemps(G):
    debut = time.time()
    max_distance = 0
    for acteur in G.nodes:
        c = sae.centralite(G, acteur)
        if c is not None and c > max_distance:
            max_distance = c
    fin = time.time()
    return round(fin-debut,5)

def temps_moy_eloignement_max(n):
    txt_jsonTemps("data/data.txt")  
    G = sae.json_vers_nx("data/data.json")
    res = 0
    for i in range(n):
        res += eloignement_maxTemps(G)
    return res/n

#print("Temps d'execution moyen de eloignemement_max:", temps_moy_eloignement_max(1), "s")
