
import json
import networkx as nx
import matplotlib.pyplot as plt


def txt_json(fichier):
    fic = open(fichier, 'r',encoding='utf8')
    fic_json = open("data.json",'w')
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
    with open("data.json", "w") as f:
        json.dump(films,f,indent=4,ensure_ascii=False)


     
#txt_json("data_100.txt")

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



G = json_vers_nx("data.json")
plt.clf()
nx.draw(G)
plt.show()


                


def collaborateurs_communs(acteurs1, acteurs2):
    with open("data.json", "r") as f:
        data = json.load(f)
    ens = set()
    for film in data:
        for acteurs in film.values():
            for acteur in acteurs:
                if acteurs1 == acteur or acteurs2 == acteur :
                    ens.update(acteurs)

    return ens




print(collaborateurs_communs("Anna Lizaran","Harrison Ford")) 

    

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
  
#ens = collaborateurs_proches(G,"Harrison Ford",2)


def est_proche(G, u, v,k=1):
    """Fonction renvoyant True si u et v sont reliés dans le graphe G, False sinon.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet
    """
    return u in collaborateurs_proches(G,v,k)


#print(est_proche(G,"John Cazale","Harrison Ford"))



def distance_naive(G, u, v):
    """ Fonction renvoyant la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet de départ, un acteur
        v (String): le sommet d'arrivée, un acteur

    Returns:
        int: la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Complexité: O(n+m) où n est le nombre de sommets et m le nombre d'arêtes du graphe.
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

#ens = collaborateurs_proches(G,"Harrison Ford",2)


def est_proche(G, u, v,k=1):
    """Fonction renvoyant True si u et v sont reliés dans le graphe G, False sinon.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet
    """
    return u in collaborateurs_proches(G,v,k)

def distance(G,u,v):
    """Fonction renvoyant la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet

    Complexité: O(n+m) où n est le nombre de sommets et m le nombre d'arêtes du graphe.
    """
    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    try:
        return nx.shortest_path_length(G,u,v) # Utilisation de la fonction de NetworkX pour calculer la distance
    except nx.NetworkXNoPath: # Si aucun chemin n'existe entre u et v
        return None


#print(est_proche(G,"John Cazale","Harrison Ford"))



def distance_naive(G, u, v):
    """ Fonction renvoyant la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet de départ, un acteur
        v (String): le sommet d'arrivée, un acteur

    Returns:
        int: la distance entre u et v dans le graphe G. La fonction renvoie None si u ou v sont absents du graphe.

    Complexité: O(n+m) où n est le nombre de sommets et m le nombre d'arêtes du graphe.
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

    Complexité: O(n+m) où n est le nombre de sommets et m le nombre d'arêtes du graphe.
    """
    if u not in G.nodes:
        return None
    if v not in G.nodes:
        return None
    try:
        return nx.shortest_path_length(G,u,v) # Utilisation de la fonction de NetworkX pour calculer la distance
    except nx.NetworkXNoPath: # Si aucun chemin n'existe entre u et v
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



def centralite(G, u):
    """Fonction renvoyant la centralité de l'acteur u dans le graphe G par rapport à la plus grande distance qui le sépare d'un autre acteur. La fonction renvoie None si u est absent du graphe.

    Args:
        G (Graphe): le graphe
        u (String): le sommet, un acteur

    Returns:
        int: la centralité de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.

    Complexité: O(N(N+E)) où N est le nombre de sommets et E le nombre d'arêtes du graphe.

    """
    if u not in G.nodes:
        return None
    centralite = 0
    for voisin in G.nodes:
        if voisin != u:
            d = distance(G,u,voisin)
            if d is not None and d > centralite:
                centralite = d
    return centralite

#print(centralite(G,"Jennifer Salt"))

    
def centre_holywood(G):
    """Fonction renvoyant l'acteur le plus central du graphe G par rapport au minimum de centralite par acteur .
    
    Parametres:
        G: le graphe
    Returns:
        str: l'acteur le plus central du graphe G
    Complexité: O(N(N+E)) où N est le nombre de sommets et E le nombre d'arêtes du graphe.
    """
    centralites = {acteur: centralite(G,acteur) for acteur in G.nodes}
    return min(centralites, key=centralites.get)

#print(centre_holywood(G)) 

