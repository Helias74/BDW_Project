"""
Ficher initialisation (eg, constantes chargées au démarrage dans la session)
"""

from datetime import datetime
from os import path

SESSION['APP'] = "CibleGrille"  # Nom de l'application
SESSION['BASELINE'] = "Défiez votre logique"  # Slogan de l'application
SESSION['DIR_HISTORIQUE'] = path.join(SESSION['DIRECTORY'], "historiques")  # Chemin pour le répertoire des historiques
SESSION['HISTORIQUE'] = dict()  # Initialisation d'un dictionnaire pour l'historique
SESSION['CURRENT_YEAR'] = datetime.now().year  # Année actuelle
SESSION["pioche"] = None
SESSION["choix"] = [] #Donne l'ID de la brique choisie 
SESSION["bool_grille"] = False #Indique si une grille a été crée 
SESSION["longueur"]  = 0 
SESSION["hauteur"]  = 0
SESSION["partie_debut"] = False #Indique si la partie est commencé
SESSION["choix_ensemble"] = [] #Ajouter pour avoir l'ensemble des valeurs sur une brique choisie 
SESSION["cible"] = -1  #Permet de gérer plus facilement les cases cible et case vide 
SESSION["case"] = -2
SESSION["nb_tours"] = 1
SESSION["changement"] = False # permet de notifier d'un changement pour regénérer la grille 
SESSION["longeur_brique_select"] = 0
SESSION["largeur_brique_select"] = 0
SESSION["grille_piece"] = [] #Grille composé de tuples avec l'id et la couleur
SESSION["tab_joueuse"] = [] #tableau contenant des tuples de type joueuses 
SESSION["mode"] = 1 #mode de jeu, init à facile
SESSION["avancement_tours"]=0
SESSION["Date_deb"] = datetime.today().date()
SESSION["Date_fin"] = datetime.today().date()
SESSION["gagnant"] = 0