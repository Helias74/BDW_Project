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