import psycopg
from model.model_pg import count_instances,top5_couleurs,score_min_max

res = count_instances(SESSION['CONNEXION'], 'piece')
if res is not None:
                nb_piece = res[0][0]
else:
    nb_piece = 0
SESSION['nb_piece'] = nb_piece
if nb_piece > 0:
    SESSION['message'] = f"{nb_piece} pièces enregistrés."
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
    SESSION['message2'] = f"{nb_boite} boites enregistrés."
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
    SESSION['message3'] = f"{nb_etape} étapes enregistrés."
else:
    SESSION['message3'] = "Aucune étape enregistré."
print (SESSION['message3'])


#Pour le top 5
#Voir le cas ou moins de 5 couleurs dans la base de donnée
res4 = top5_couleurs(SESSION['CONNEXION'])
if res4 is not None:
                SESSION['top5_couleurs'] = res4
else:
    SESSION['top5_couleurs'] = "Aucune couleurs n'est enregistré."
    

#Pour les scores des joueuses
res5 = score_min_max(SESSION['CONNEXION'])
SESSION['liste_score_min_max']=res5
print ("res 5 en bas")
print (res5)
