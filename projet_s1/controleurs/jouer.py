import psycopg
import random
from model.model_pg import get_briques_pour_pioche, get_briques_pour_pioche_maj

 
if SESSION["pioche"] is None:
    res = get_briques_pour_pioche(SESSION["CONNEXION"])
    if res is not None:
                SESSION["pioche"] = res
                tab_pioche = res
    else:
        SESSION["pioche"] = "Pas suffisament de brique disponible et compatible pour former la pioche."
        
if "brique_id" in GET:
    for i in range (4):
        if SESSION["pioche"][i][0]==int(GET["brique_id"][0]):
            SESSION["choix"].append(SESSION["pioche"][i][0])
            res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            while res3 in SESSION["choix"]:
                res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            SESSION["pioche"][i]=res3[0]


if  SESSION["grille"][0][0] is None:
    for i in range (9):
        for j in range (8):
            SESSION["grille"][i][j]=True
    N=36
    c=0
    while c!=N:
        i=random.randint(0,8)
        j=random.randint(0,7)
        if  SESSION["grille"][i][j] == True:
            SESSION["grille"][i][j]=False
            c+=1
        
        

"""
Vérification pour mise en session des choix de la joueuse 
print ("affichage de la session choix ")
for i in range (len(SESSION["choix"])):
    print ("affichage de la session choix")
    print (SESSION["choix"][i])
"""

   
    
    





