import psycopg
from model.model_pg import count_instances,top5_couleurs,score_min_max,min_max_defausse,min_max_pioche

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


res2 = count_instances(SESSION['CONNEXION'], 'participation')
print ("res2  en dessous")
print (res2)
if res2 is not None:
                nb_participation = res2[0][0]
else:
    nb_participation = 0
SESSION['nb_piece'] = nb_participation
if nb_participation > 0:
    SESSION['message2'] = f"{nb_participation} participation de joueuses à des parties."
else:
    SESSION['message2'] = "Aucune joueuse n'a participé à une partie."
print (SESSION['message2'])

res3 = count_instances(SESSION['CONNEXION'], 'joueuse')
if res3 is not None:
                nb_joueuse= res3[0][0]
else:
    nb_joueuse = 0
SESSION['nb_piece'] = nb_joueuse
if nb_joueuse > 0:
    SESSION['message3'] = f"{nb_joueuse} joueuse dans le jeu actuellement."
else:
    SESSION['message3'] = "Aucune joueuse dans le jeu actuellement."
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


#Pour défausser et piocher
res6=min_max_defausse(SESSION['CONNEXION'])
res7=min_max_pioche(SESSION['CONNEXION'])
SESSION['min_max_defausse']=res6
print ("res 6 en bas")
print (res6)
SESSION['min_max_pioche']=res7


if res6 is not None:
                SESSION['min_max_defausse'] =  f"{res6} est la partie avec le moins de pièces déffaussé."
else:
    SESSION['min_max_defausse'] = "Aucune pièce n'est enregisté."
    
