from SAE_Graphes import * 


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
    with open("data/data.json", "w") as f:
        json.dump(films,f,indent=4,ensure_ascii=False)
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_txt_json(n):
    res = 0
    for i in range(n):
        res += txt_jsonTemps("data/data.txt")
    return res/n
print("Temps d'execution moyen de txt_json",temps_moy_txt_json(100),"s")

def json_vers_nxTemps(chemin):
    debut = time.time()
    G = nx.Graph()
    with open(chemin, "r") as f:
        data = json.load(f)
        for film in data:
            acteurs = film.get("collaborateurs", [])
            for i in range(len(acteurs)):
                for j in range(i+1, len(acteurs)):
                    G.add_edge(acteurs[i], acteurs[j])
    fin = time.time()
    return round(fin-debut,10)


def temps_moy_json_nx(n):
    res = 0
    for i in range(n):
        res += json_vers_nxTemps("data/data.txt")
    return res/n
print("Temps d'execution de json_vers_nx",temps_moy_json_nx("data/data.json"),"s")

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
    
    
    return round(fin-debut,10)

def temps_moy_collaborateurs(n):
    res = 0
    for i in range(n):
        res+= collaborateurs_communsTemps("Ben Affleck", "Henry Cavill")
    return res/n
print("Temps d'execution moyen de collaborateurs commun",temps_moy_collaborateurs(100),"s") 

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
    return round(fin-debut,10)

def temps_moy_collaborateurs_proches(n):
    res = 0
    for i in range(n):
        res += collaborateurs_prochesTemps(G, "Ben Affleck", 2)
    return res/n

print("Temps d'execution moyen de collaborateurs proches:", temps_moy_collaborateurs_proches(100), "s")


def est_procheTemps(G, u, v, k=1):
    debut = time.time()
    res = u in collaborateurs_proches(G, v, k)
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_est_proche(n):
    res = 0
    for i in range(n):
        res += est_procheTemps(G, "John Cazale", "Harrison Ford", 2)
    return res/n

print("Temps d'execution moyen de est proche:", temps_moy_est_proche(100), "s")

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
                    return round(fin-debut,10)
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        
        if not collaborateurs_directs:
            return None
        collaborateurs = collaborateurs_directs
        n += 1
    
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_distance_naive(n):
    res = 0
    for i in range(n):
        res += distance_naiveTemps(G, "Harrison Ford", "John Cazale")
    return res/n

print("Temps d'execution moyen de distance naive:", temps_moy_distance_naive(100), "s")

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
    return round(fin-debut,10)

def temps_moy_distance(n):
    res = 0
    for i in range(n):
        res += distanceTemps(G, "Harrison Ford", "John Cazale")
    return res/n

print("Temps d'execution moyen de distance:", temps_moy_distance(100), "s")

def distance2Temps(G, u, v):
    debut = time.time()
    if u not in G.nodes or v not in G.nodes:
        return None
    
    visite = set()
    queue = [(u, 0)]

    while queue:
        node, dist = queue.pop(0)
        if node == v:
            fin = time.time()
            return round(fin-debut,10)
        if node not in visite:
            visite.add(node)
            for neighbor in G.neighbors(node):
                queue.append((neighbor, dist + 1))
    
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_distance2(n):
    res = 0
    for i in range(n):
        res += distance2Temps(G, "Harrison Ford", "John Cazale")
    return res/n

print("Temps d'execution moyen de distance2:", temps_moy_distance2(100), "s")

def centraliteTemps(G, u):
    debut = time.time()
    if u not in G.nodes:
        return None
    
    dico = {u : 0}
    a_traiter = [u]
    while a_traiter:
        sommet = a_traiter.pop(0)
        for voisin in G.adj[sommet]:
            if voisin not in dico:
                dico[voisin] = dico[sommet] + 1
                a_traiter.append(voisin)
    
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_centralite(n):
    res = 0
    for i in range(n):
        res += centraliteTemps(G, "Jennifer Salt")
    return res/n

print("Temps d'execution moyen de centralite:", temps_moy_centralite(10), "s")

data10000 = txt_json("data/data_10000.txt")
G2= json_vers_nx("data/data.json")
def centre_holywoodTemps(G):
    debut = time.time()
    centralites = {acteur: centralite(G,acteur) for acteur in G.nodes}
    centre = min(centralites, key=centralites.get)
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_centre_holywood(n,G2):
    res = 0
    for i in range(n):
        res += centre_holywoodTemps(G)
    return res/n

print("Temps d'execution moyen de centre_holywood:", temps_moy_centre_holywood(1,G2), "s")


def eloignement_maxTemps(G):
    debut = time.time()
    max_distance = 0
    for acteur in G.nodes:
        c = centralite(G, acteur)
        if c is not None and c > max_distance:
            max_distance = c
    fin = time.time()
    return round(fin-debut,10)

def temps_moy_eloignement_max(n):

    res = 0
    for i in range(n):
        res += eloignement_maxTemps(G2)
    return res/n

print("Temps d'execution moyen de eloignemement_max:", temps_moy_eloignement_max(1,G2), "s")