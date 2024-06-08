import requetes as r 
import json
import networkx as nx
import matplotlib.pyplot as plt

def Appli_oracle():
    """
    Application interactive pour poser des questions sur les relations entre acteurs de cinéma.

    Cette fonction charge initialement un petit jeu de données et offre une interface utilisateur
    pour interagir avec les données du graphe d'acteurs. L'utilisateur peut poser des questions
    sur les relations entre les acteurs, visualiser des graphes et changer le jeu de données.
    """
    
    # Chargement initial des données
    json = r.txt_json("data/data_100.txt")
    G = r.json_vers_nx("data/data.json")

    while True:
        # Affichage du menu
        print("Bienvenue dans l'application Oracle")
        print("Vous pouvez poser des questions sur les acteurs de cinéma.")
        print("Tapez 'q' pour quitter l'application.")
        print("Tapez 'z' pour choisir quantite de donnée.")
        print("Tapez 'r' pour savoir si deux acteurs sont reliés.")
        print("Tapez 'p' pour savoir si deux acteurs sont à distance au plus k.")
        print("Tapez 'd' pour connaître la distance entre deux acteurs.")
        print("Tapez 'c' pour connaître la centralité de l'acteur.")
        print("Tapez 's' pour connaître l'acteur le plus central.")
        print("Tapez 'h' pour obtenir de l'aide.")
        print("Tapez 'g' pour afficher le graphe.")
        print("Tapez 'a' pour afficher le graphe d'un acteur.")
        
        # Lecture du choix utilisateur
        choix = str(input("Que voulez-vous faire?"))
        
        if choix == "q":
            # Quitter l'application
            print("Merci d'avoir utilisé l'application.")
            break
        elif choix == "r":
            # Vérifier si deux acteurs sont reliés
            acteur1 = input("Entrez le nom du premier acteur:")
            acteur2 = input("Entrez le nom du second acteur:")
            print(r.est_proche(G, acteur1, acteur2))
        elif choix == "p":
            # Vérifier si deux acteurs sont à distance au plus k
            acteur1 = input("Entrez le nom du premier acteur:")
            acteur2 = input("Entrez le nom du second acteur:")
            k = int(input("Entrez la distance maximale:"))
            print(r.est_proche(G, acteur1, acteur2, k))
        elif choix == "g":
            # Afficher le graphe complet
            print("Affichage du graphe.")
            plt.clf()
            nx.draw(G)
            plt.show()
        elif choix == "d":
            # Connaître la distance entre deux acteurs
            acteur1 = input("Entrez le nom du premier acteur:")
            acteur2 = input("Entrez le nom du second acteur:")
            print(r.distance(G, acteur1, acteur2))
        elif choix == "c":
            # Connaître la centralité d'un acteur
            acteur = input("Entrez le nom de l'acteur:")
            print(r.centralite(G, acteur))
        elif choix == "s":
            # Connaître l'acteur le plus central
            print(r.centre_holywood(G))
        elif choix == "a":
            # Afficher le graphe d'un acteur à distance k
            acteur = input("Entrez le nom de l'acteur:")
            k = int(input("Entrez la distance maximale:"))
            print("Affichage du graphe.")
            ens = r.collaborateurs_proches(G, acteur, k)
            plt.clf()
            nx.draw(G.subgraph(ens))
            plt.show()
        elif choix == "z":
            # Choisir la quantité de données
            print("Tapez '100' pour le jeu de 100 données")
            print("Tapez '1000' pour le jeu de 1000 données")
            print("Tapez '10000' pour le jeu de 10000 données")
            print("Tapez 't' pour le jeu de données complet")
            choix_donnees = str(input("Choisissez la quantité de données:"))
            
            if choix_donnees == "100":
                json = r.txt_json("data/data_100.txt")
                G = r.json_vers_nx("data/data.json")
            elif choix_donnees == "1000":
                json = r.txt_json("data/data_1000.txt")
                G = r.json_vers_nx("data/data.json")
            elif choix_donnees == "10000":
                json = r.txt_json("data/data_10000.txt")
                G = r.json_vers_nx("data/data.json")
            elif choix_donnees == "t":
                json = r.txt_json("data/data.txt")
                G = r.json_vers_nx("data/data.json")
            else:
                print("Commande inconnue.")
        elif choix == "h":
            # Afficher l'aide
            print("Tapez 'q' pour quitter l'application.")
            print("Tapez 'r' pour savoir si deux acteurs sont reliés.")
            print("Tapez 'p' pour savoir si deux acteurs sont à distance au plus k.")
            print("Tapez 'd' pour connaître la distance entre deux acteurs.")
            print("Tapez 'c' pour connaître la centralité de l'acteur.")
            print("Tapez 's' pour connaître l'acteur le plus central.")
            print("Tapez 'g' pour afficher le graphe.")
            print("Tapez 'a' pour afficher le graphe d'un acteur.")
            print("Tapez 'z' pour choisir quantite de donnée.")
        else:
            print("Commande inconnue.")

Appli_oracle()
