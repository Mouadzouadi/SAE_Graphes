
import json
import networkx as nx
import matplotlib.pyplot as plt
import time 

def txt_json(fichier):
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
    with open("data/data.json", "w") as f:
        json.dump(films,f,indent=4,ensure_ascii=False)


     
txt_json("data/data_100.txt")

def json_vers_nx(chemin):
    G = nx.Graph()
    with open(chemin, "r") as f:
        data = json.load(f)
        for film in data:
            acteurs = film.get("collaborateurs", [])
            for i in range(len(acteurs)):
                for j in range(i+1, len(acteurs)):
                    G.add_edge(acteurs[i], acteurs[j])
    return G

G = json_vers_nx("data/data.json")

#plt.clf()
#nx.draw(G, with_labels=True)
#plt.show()


                


def collaborateurs_communs(acteurs1, acteurs2):
    
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
    
    return ens
#print(collaborateurs_communs("Ben Affleck","Henry Cavill"))


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

def distance2(G,u,v):
    """Fonction renvoyant la distance entre u et v dans le graphe G. 
    La fonction renvoie None si u ou v sont absents du graphe.
    Sans utiliser la fonction de NetworkX.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet

    Complexité: O(n+e) où n est le nombre de sommets et E le nombre d'arêtes du graphe.
    """
    debut_calcul = time.time()
    if u not in G.nodes:
        print(u, "est absent du graphe.")
        return None
    if v not in G.nodes:
        print(v, "est absent du graphe.")
        return None
    
    visite = set()
    queue = [(u, 0)]

    while queue:
        node, dist = queue.pop(0)
        if node == v:
            return dist
        if node not in visite:
            visite.add(node)
            for neighbor in G.neighbors(node):
                queue.append((neighbor, dist + 1))

    return None

#print(distance(G,"Harrison Ford","John Cazale"))
#print(distance2(G,"Harrison Ford","John Cazale"))


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

#print(centralite(G,"Jennifer Salt"))

    
def centre_holywood(G):
    """Fonction renvoyant l'acteur le plus central du graphe G par rapport au minimum de centralite par acteur .
    
    Parametres:
        G: le graphe
    Returns:
        str: l'acteur le plus central du graphe G
    Complexité: O(N^2+NE)) où N est le nombre de sommets et E le nombre d'arêtes du graphe.
    """

    centralites = {acteur: centralite(G,acteur) for acteur in G.nodes}
    centre = min(centralites, key=centralites.get)
    return centre

#print(centre_holywood(G)) 


def eloignement_max(G):
    """Fonction renvoyant la distance maximale entre deux acteurs du graphe G .
    Parametres:
        G: le graphe
    Returns:
        int: la distance maximale entre deux acteurs du graphe G

    Complexité: O(N^2+ N*E) où N est le nombre de sommets et E le nombre d'arêtes du graphe.
    """

    max_distance = 0
    for acteur in G.nodes:
        c = centralite(G, acteur)
        if c is not None and c > max_distance:
            max_distance = c


    return max_distance

#print(eloignement_max(G))

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