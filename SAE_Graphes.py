import json
def txt_json(fichier):
    fic = open(fichier, 'r',encoding='utf8')
    fic_json = open("data.json",'w')
    lignes = fic.readlines()
    films = []
    for ligne in lignes:
        data = json.loads(ligne)
        modif = {}
        for titre, valeur in data.items():
            liste = []
            if type(valeur) == list :
                for carac in valeur:
                    carac = carac.strip('"').replace("[[", "")
                    carac =carac.strip('"').replace("]]", "")
                    liste.append(carac)
                modif[titre] = liste
            if type(valeur) == str:
                modif[titre] = valeur
            films.append(modif)
    with open("data.json", "w") as f:
        json.dump(films,f,indent=4,ensure_ascii=False)

    

     
txt_json("data_2.txt")

