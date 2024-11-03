"""
import psycopg
from model.model_pg import count_instances
connexion = psycopg.connect(
    dbname="p2309994",      # Nom de votre base de données
    user="p2309994",        # Nom d'utilisateur PostgreSQL
    password="Watch55During",    # Mot de passe PostgreSQL
    host="bd-pedago.univ-lyon1.fr",                # Adresse du serveur, généralement "localhost" pour une base locale
    port="5432"                      # Port de PostgreSQL, par défaut "5432"
)


def afficher_acceuil(connexion):
    # Compte le nombre d'instances dans les tables souhaitées
    nb_brique = count_instances(connexion, 'brique')
    nb_piece = count_instances(connexion, 'piece')
    nb_parties = count_instances(connexion, 'partie')

    # Passe les résultats au template acceuil.html
    return render_template('acceuil.html', nb_brique=nb_brique, nb_piece=nb_piece, nb_parties=nb_parties)

"""


"""
# Connexion à la base de données
connexion = psycopg.connect(
    dbname="p2309994",                 # Nom de votre base de données
    user="p2309994",                   # Nom d'utilisateur PostgreSQL
    password="Watch55During",          # Mot de passe PostgreSQL
    host="bd-pedago.univ-lyon1.fr",    # Adresse du serveur
    port="5432"                        # Port de PostgreSQL
)
print (connexion)
"""

import psycopg
from model.model_pg import count_instances,top5_couleurs

res = count_instances(SESSION['CONNEXION'], 'piece')
if res is not None:
                nb_piece = res[0][0]
else:
    nb_piece = 0
SESSION['nb_piece'] = nb_piece
if nb_piece > 0:
    SESSION['message'] = f"Actuellement {nb_piece} pièces enregistrés."
else:
    SESSION['message'] = "Aucune pièce enregistré."
print (SESSION['message'])


res2 = count_instances(SESSION['CONNEXION'], 'boite')
if res2 is not None:
                nb_boite = res2[0][0]
else:
    nb_boite = 0
SESSION['nb_piece'] = nb_boite
if nb_boite > 0:
    SESSION['message2'] = f"Actuellement {nb_boite} boites enregistrés."
else:
    SESSION['message2'] = "Aucune boite enregistré."
print (SESSION['message2'])

res3 = count_instances(SESSION['CONNEXION'], 'etape')
if res3 is not None:
                nb_etape = res3[0][0]
else:
    nb_etape = 0
SESSION['nb_piece'] = nb_etape
if nb_etape > 0:
    SESSION['message3'] = f"Actuellement {nb_etape} étapes enregistrés."
else:
    SESSION['message3'] = "Aucune étape enregistré."
print (SESSION['message3'])



#Voir le cas ou moins de 5 couleurs dans la base de donnée
res4 = top5_couleurs(SESSION['CONNEXION'])
if res3 is not None:
                SESSION['top5_couleurs'] = res4
else:
    SESSION['top5_couleurs'] = "Aucune couleurs n'est enregistré enregistré."


