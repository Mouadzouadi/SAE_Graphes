
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


     
txt_json("data_100.txt")

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

ens = collaborateurs_proches(G,"Alexy wiciak",2)


def est_proche(G, u, v,k):
    """Fonction renvoyant True si u et v sont reliés dans le graphe G, False sinon.
    
    Parametres:
        G: le graphe
        u: un sommet
        v: un sommet
    """
    return u in collaborateurs_proches(G,v,k)


print(est_proche(G,"John Cazale","Harrison Ford"))
