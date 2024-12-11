import psycopg
import random
from model.model_pg import get_briques_pour_pioche, get_briques_pour_pioche_maj

###Pour la gestion de lancement de la partie 
if "longueur_grille" in GET and "hauteur_grille" in GET:
    SESSION["partie_debut"] = True

###Pour gérer la fin de partie 

if "quitter" in GET:
    if GET["quitter"][0] == "confirmer":
        SESSION["partie_debut"] = False
    






         



"""
Vérification pour mise en session des choix de la joueuse 
print ("affichage de la session choix ")
for i in range (len(SESSION["choix"])):
    print ("affichage de la session choix")
    print (SESSION["choix"][i])
"""




###Codage de la grille 

#Pour choix de la direction 
haut = 0
bas = 2
droite = 1
gauche = 3


#Initialisation de la grille
if "longueur_grille" in GET and "hauteur_grille" in GET:
    if SESSION["longueur"] != int(GET["longueur_grille"][0]) or SESSION["hauteur"] != int(GET["hauteur_grille"][0]) or SESSION["changement"] == True:
        SESSION["bool_grille"]=False
    if SESSION["bool_grille"]==False:
        SESSION["longueur"] = int(GET["longueur_grille"][0])
        SESSION["hauteur"] = int(GET["hauteur_grille"][0])
        SESSION["grille"] = [[SESSION["case"] for _ in range(SESSION["longueur"])] for _ in range(SESSION["hauteur"])]
        for i in range  (SESSION["hauteur"]):
            for j in range (SESSION["longueur"]):
                SESSION["grille"][i][j]=SESSION["case"]
        #Pour le nb de cibles 
        nb = 0
        nb = SESSION["longueur"] * SESSION["hauteur"]
        rand = random.randint(1,2)
        div = rand/10
        if rand ==1:
            nb = int(nb * div) + 1  
        else:
            nb = int(nb * div)
        #Mise d'une cible

        l=random.randint(0, SESSION["longueur"]-1)
        h=random.randint(0, SESSION["hauteur"]-1)
        SESSION["grille"][h][l] = SESSION["cible"]
        nb-=1
        #Ajout des autres cibles
        while nb>0 :
            nb_provisoir=nb
            memoire_direction=[]
            while len (memoire_direction)<4 and nb_provisoir==nb:
                direction  = random.randint(0,3)
            
                if direction == haut:
                    if h-1>=0 :
                        if SESSION["grille"][h-1][l] == SESSION["case"]:
                            SESSION["grille"][h-1][l] = SESSION["cible"]
                            h=h-1
                            nb_provisoir-=1      
                    if h-1<0 or SESSION["grille"][h-1][l] == SESSION["cible"]:       
                        if haut not in memoire_direction:
                            memoire_direction.append(haut)
                        
            
                if direction == droite:
                    if l+1<=SESSION["longueur"]-1 :
                        if SESSION["grille"][h][l+1] == SESSION["case"]:
                            SESSION["grille"][h][l+1] = SESSION["cible"]
                            l=l+1
                            nb_provisoir-=1
                    if l+1>SESSION["longueur"]-1 or SESSION["grille"][h][l+1] == SESSION["cible"]:        
                        if droite not in memoire_direction:
                            memoire_direction.append(droite)
                    
                if direction == bas:
                    if h+1<=SESSION["hauteur"]-1:
                        if SESSION["grille"][h+1][l] == SESSION["case"]:
                            SESSION["grille"][h+1][l] = SESSION["cible"]
                            h=h+1
                            nb_provisoir-=1
                    if h+1>SESSION["hauteur"]-1 or SESSION["grille"][h+1][l] == SESSION["cible"]:         
                        if bas not in memoire_direction:
                            memoire_direction.append(bas)
                    
                if direction == gauche:
                    if l-1>=0 :
                        if SESSION["grille"][h][l-1] == SESSION["case"]:
                            SESSION["grille"][h][l-1] = SESSION["cible"]
                            l=l-1
                            nb_provisoir-=1 
                    if l-1<0 or SESSION["grille"][h][l-1] == SESSION["cible"]:        
                        if gauche not in memoire_direction:
                            memoire_direction.append(gauche)
            if  len (memoire_direction)>=4:
                nb=0
            else:
                nb=nb_provisoir        
    
    SESSION["bool_grille"]=True
        
  
####GESTION DES PLACEMENTS SUR LA GRILLE 


###Pour la gestion de la pioche 
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
            SESSION["choix_ensemble"].append(SESSION["pioche"][i])
            res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            while res3 in SESSION["choix"]:
                res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            SESSION["pioche"][i]=res3[0]
            
            ###Pour obtenir la longeur et la largeur de la brique sélectionné
            SESSION["longeur_brique_select"] = int (SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][1])
            SESSION["largeur_brique_select"] = int (SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][2])
            print (SESSION["longeur_brique_select"])
            print (SESSION["largeur_brique_select"])

##Pour obtenir le choix du joueur sur la position de la pièce 
if "x" in GET and "y" in GET:
    SESSION["posx"] = int(GET["x"][0])
    SESSION["posy"] = int(GET["y"][0])
    ##Pour Vérifier si le placement choisie est possible 
    b=True
    for i in range (SESSION["longeur_brique_select"]):
        for j in range(SESSION["largeur_brique_select"]):
            if SESSION["grille"][SESSION["posx"]+i][SESSION["posy"]+j]!=SESSION["cible"]:
                print ("test de la validité du placement ")
                b=False
    #Changement de tours et placement 
    if b==False:
        SESSION["nb_tours"]-=1
        print ("Aucune piece n'a été placé")
    else:
        for i in range (SESSION["longeur_brique_select"]):
            for j in range(SESSION["largeur_brique_select"]):
                SESSION["grille"][SESSION["posx"]+i][SESSION["posy"]+j] = SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][0]
        SESSION["changement"] = True
        SESSION["nb_tours"]-=1
        print ("une piece a été placé")





   
    
    





