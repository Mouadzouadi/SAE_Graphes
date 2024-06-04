import json
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import threading
import SAE_Graphes as r

class ApplicationOracle:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Oracle")
        self.root.geometry("500x700")
        
        self.dataset_options = ["data/data_100.txt", "data/data_1000.txt", "data/data_10000.txt", "data/data.txt"]
        self.dataset_file = tk.StringVar(value=self.dataset_options[0])  # Jeu de données par défaut
        
        self.charger_donnees()  # Charger les données initiales
        self.creer_widgets()  # Créer les widgets de l'interface utilisateur
    
    def charger_donnees(self):
        try:
            # Charger les données du fichier sélectionné et créer le graphe
            r.txt_json(self.dataset_file.get())
            self.G = r.json_vers_nx("data/data.json")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des données: {e}")
    
    def creer_widgets(self):
        options_padding = {'padx': 10, 'pady': 10}
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 12), padding=10)
        style.configure('TOptionMenu', font=('Helvetica', 12), padding=10)

        # Créer et positionner les widgets avec padding
        ttk.Label(self.root, text="Bienvenue dans l'application Oracle", style='TLabel').grid(row=0, column=0, columnspan=2, **options_padding)
        
        # OptionMenu pour choisir le jeu de données
        ttk.Label(self.root, text="Choisir le jeu de données:", style='TLabel').grid(row=1, column=0, **options_padding)
        dataset_menu = ttk.OptionMenu(self.root, self.dataset_file, *self.dataset_options, command=self.charger_nouveau_dataset)
        dataset_menu.grid(row=1, column=1, **options_padding)
        
        # Créer des boutons avec style
        ttk.Button(self.root, text="Relier deux acteurs", command=self.verifier_relie).grid(row=2, column=0, **options_padding)
        ttk.Button(self.root, text="Distance au plus k", command=self.verifier_distance_k).grid(row=3, column=0, **options_padding)
        ttk.Button(self.root, text="Distance entre deux acteurs", command=self.verifier_distance).grid(row=4, column=0, **options_padding)
        ttk.Button(self.root, text="Centralité d'un acteur", command=self.verifier_centralite).grid(row=5, column=0, **options_padding)
        ttk.Button(self.root, text="Acteur le plus central", command=self.acteur_le_plus_central).grid(row=6, column=0, **options_padding)
        ttk.Button(self.root, text="Afficher le graphe", command=self.afficher_graphe).grid(row=7, column=0, **options_padding)
        ttk.Button(self.root, text="Collaborateurs proches", command=self.afficher_collaborateurs_proches).grid(row=8, column=0, **options_padding)
        ttk.Button(self.root, text="Quitter", command=self.root.quit).grid(row=9, column=0, **options_padding)
    
    def afficher_message_patience(self):
        # Afficher un message de patience
        self.label_patience = ttk.Label(self.root, text="Veuillez patienter...", style='TLabel')
        self.label_patience.grid(row=10, column=0, columnspan=2, pady=10)
        self.root.update()

    def masquer_message_patience(self):
        # Masquer le message de patience
        self.label_patience.grid_forget()
    
    def charger_nouveau_dataset(self, event):
        try:
            # Recharger les données avec le nouveau jeu de données sélectionné
            self.charger_donnees()
            messagebox.showinfo("Info", f"Jeu de données {self.dataset_file.get()} chargé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement du jeu de données: {e}")
    
    def verifier_relie(self):
        # Demander les noms des deux acteurs
        acteur1 = simpledialog.askstring("Input", "Entrez le nom du premier acteur:")
        acteur2 = simpledialog.askstring("Input", "Entrez le nom du second acteur:")
        if acteur1 and acteur2:
            self.afficher_message_patience()  # Afficher un message de patience
            # Lancer un nouveau thread pour vérifier si les acteurs sont reliés
            threading.Thread(target=self.verifier_relie_thread, args=(acteur1, acteur2)).start()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer les noms des deux acteurs.")
    
    def verifier_relie_thread(self, acteur1, acteur2):
        try:
            # Vérifier si les acteurs sont reliés et afficher le résultat
            resultat = r.est_proche(self.G, acteur1, acteur2)
            self.masquer_message_patience()  # Masquer le message de patience
            # Afficher le résultat dans une boîte de dialogue
            messagebox.showinfo("Résultat", f"Les acteurs {acteur1} et {acteur2} sont-ils reliés ?\n\n{'Oui' if resultat else 'Non'}")
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors de la vérification de la relation: {e}")
    
    def verifier_distance_k(self):
        # Demander les noms des deux acteurs et la distance maximale
        acteur1 = simpledialog.askstring("Input", "Entrez le nom du premier acteur:")
        acteur2 = simpledialog.askstring("Input", "Entrez le nom du second acteur:")
        k = simpledialog.askinteger("Input", "Entrez la distance maximale:")
        if acteur1 and acteur2 and k is not None:
            self.afficher_message_patience()  # Afficher un message de patience
            # Lancer un nouveau thread pour vérifier la distance au plus k
            threading.Thread(target=self.verifier_distance_k_thread, args=(acteur1, acteur2, k)).start()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer les noms des deux acteurs et une distance valide.")
    
    def verifier_distance_k_thread(self, acteur1, acteur2, k):
        try:
            # Vérifier si les acteurs sont à une distance au plus de k et afficher le résultat
            resultat = r.est_proche(self.G, acteur1, acteur2, k)
            self.masquer_message_patience()  # Masquer le message de patience
            # Afficher le résultat dans une boîte de dialogue
            messagebox.showinfo("Résultat", f"Les acteurs {acteur1} et {acteur2} sont-ils à une distance au plus de {k} ?\n\n{'Oui' if resultat else 'Non'}")
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors de la vérification de la distance: {e}")
    
    def verifier_distance(self):
        # Demander les noms des deux acteurs
        acteur1 = simpledialog.askstring("Input", "Entrez le nom du premier acteur:")
        acteur2 = simpledialog.askstring("Input", "Entrez le nom du second acteur:")
        if acteur1 and acteur2:
            self.afficher_message_patience()  # Afficher un message de patience
            # Lancer un nouveau thread pour vérifier la distance entre les acteurs
            threading.Thread(target=self.verifier_distance_thread, args=(acteur1, acteur2)).start()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer les noms des deux acteurs.")
    
    def verifier_distance_thread(self, acteur1, acteur2):
        try:
            # Calculer la distance entre les deux acteurs et afficher le résultat
            resultat = r.distance(self.G, acteur1, acteur2)
            self.masquer_message_patience()  # Masquer le message de patience
            if resultat is not None:
                # Afficher le résultat dans une boîte de dialogue
                messagebox.showinfo("Résultat", f"La distance entre {acteur1} et {acteur2} est de {resultat}.")
            else:
                messagebox.showinfo("Résultat", f"Aucun chemin trouvé entre {acteur1} et {acteur2}.")
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors du calcul de la distance: {e}")
    
    def verifier_centralite(self):
        # Demander le nom de l'acteur
        acteur = simpledialog.askstring("Input", "Entrez le nom de l'acteur:")
        if acteur:
            self.afficher_message_patience()  # Afficher un message de patience
            # Lancer un nouveau thread pour vérifier la centralité de l'acteur
            threading.Thread(target=self.verifier_centralite_thread, args=(acteur,)).start()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer le nom de l'acteur.")
    
    def verifier_centralite_thread(self, acteur):
        try:
            # Calculer la centralité de l'acteur et afficher le résultat
            resultat = r.centralite(self.G, acteur)
            self.masquer_message_patience()  # Masquer le message de patience
            if resultat is not None:
                # Afficher le résultat dans une boîte de dialogue
                messagebox.showinfo("Résultat", f"La centralité de {acteur} est de {resultat}.")
            else:
                messagebox.showinfo("Résultat", f"Aucun chemin trouvé pour l'acteur {acteur}.")
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors du calcul de la centralité: {e}")
    
    def acteur_le_plus_central(self):
        # Calculer l'acteur le plus central
        self.afficher_message_patience()  # Afficher un message de patience
        # Lancer un nouveau thread pour trouver l'acteur le plus central
        threading.Thread(target=self.acteur_le_plus_central_thread).start()
    
    def acteur_le_plus_central_thread(self):
        try:
            # Afficher l'acteur le plus central
            resultat = r.centre_holywood(self.G)
            self.masquer_message_patience()  # Masquer le message de patience
            # Afficher le résultat dans une boîte de dialogue
            messagebox.showinfo("Résultat", f"L'acteur le plus central est {resultat}.")
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors de la recherche de l'acteur le plus central: {e}")
    
    def afficher_graphe(self):
        # Afficher le graphe
        self.afficher_message_patience()  # Afficher un message de patience
        # Lancer un nouveau thread pour afficher le graphe
        threading.Thread(target=self.afficher_graphe_thread).start()
    
    def afficher_graphe_thread(self):
        try:
            # Dessiner et afficher le graphe
            plt.clf()  # Nettoyer la figure
            nx.draw(self.G, with_labels=True)  # Dessiner le graphe avec les étiquettes des nœuds
            plt.show()  # Afficher la figure
            self.masquer_message_patience()  # Masquer le message de patience
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphe: {e}")
    
    def afficher_collaborateurs_proches(self):
        # Demander le nom de l'acteur et la distance maximale
        acteur = simpledialog.askstring("Input", "Entrez le nom de l'acteur:")
        k = simpledialog.askinteger("Input", "Entrez la distance maximale:")
        if acteur and k is not None:
            self.afficher_message_patience()  # Afficher un message de patience
            # Lancer un nouveau thread pour afficher les collaborateurs proches
            threading.Thread(target=self.afficher_collaborateurs_proches_thread, args=(acteur, k)).start()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer un nom d'acteur et une distance valide.")
    
    def afficher_collaborateurs_proches_thread(self, acteur, k):
        try:
            # Calculer et afficher le sous-graphe des collaborateurs proches
            ens = r.collaborateurs_proches(self.G, acteur, k)
            sous_graphe = self.G.subgraph(ens)
            self.masquer_message_patience()  # Masquer le message de patience
            plt.clf()
            nx.draw(sous_graphe, with_labels=True)
            plt.show()
        except Exception as e:
            self.masquer_message_patience()  # Masquer le message de patience
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des collaborateurs proches: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationOracle(root)
    root.mainloop()
