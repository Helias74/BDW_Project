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

"""
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
 



#Pour choix de la direction 
haut = 0
bas = 2
droite = 1
gauche = 3


#Initialisation de la grille
if "longueur_grille" in GET and "hauteur_grille" in GET:
    if SESSION["longueur"] != int(GET["longueur_grille"][0]) or SESSION["hauteur"] != int(GET["hauteur_grille"][0]):
        SESSION["bool_grille"]=False
    if SESSION["bool_grille"]==False:
        SESSION["longueur"] = int(GET["longueur_grille"][0])
        SESSION["hauteur"] = int(GET["hauteur_grille"][0])
        SESSION["grille"] = [[True for _ in range(SESSION["longueur"])] for _ in range(SESSION["hauteur"])]
        for i in range  (SESSION["hauteur"]):
            for j in range (SESSION["longueur"]):
                SESSION["grille"][i][j]=True
        #Pour le nb de cibles 
        nb = 0
        nb = SESSION["longueur"] * SESSION["hauteur"]
        rand = random.randint(1,2)
        div = rand
        div = div/10
        if rand ==1:
            nb = int(nb * div) + 1  
        else:
            nb = int(nb * div)
        #Mise d'une cible pour test

        l=random.randint(0, SESSION["longueur"]-1)
        h=random.randint(0, SESSION["hauteur"]-1)
        SESSION["grille"][h][l] = False
        nb-=1
        
        
        while nb>0 :
            nb_provisoir=nb
            memoire_direction=[]
            while len (memoire_direction)<4 and nb_provisoir==nb:
                direction  = random.randint(0,3)
            
                if direction == haut:
                    if h-1>=0 :
                        if SESSION["grille"][h-1][l] == True:
                            SESSION["grille"][h-1][l] = False
                            h=h-1
                            nb_provisoir-=1      
                    if h-1<0 or SESSION["grille"][h-1][l] == False:       
                        if haut not in memoire_direction:
                            memoire_direction.append(haut)
                        
            
                if direction == droite:
                    if l+1<=SESSION["longueur"]-1 :
                        if SESSION["grille"][h][l+1] == True:
                            SESSION["grille"][h][l+1] = False
                            l=l+1
                            nb_provisoir-=1
                    if l+1>SESSION["longueur"]-1 or SESSION["grille"][h][l+1] == False:        
                        if droite not in memoire_direction:
                            memoire_direction.append(droite)
                    
                if direction == bas:
                    if h+1<=SESSION["hauteur"]-1:
                        if SESSION["grille"][h+1][l] == True:
                            SESSION["grille"][h+1][l] = False
                            h=h+1
                            nb_provisoir-=1
                    if h+1>SESSION["hauteur"]-1 or SESSION["grille"][h+1][l] == False:         
                        if bas not in memoire_direction:
                            memoire_direction.append(bas)
                    
                if direction == gauche:
                    if l-1>=0 :
                        if SESSION["grille"][h][l-1] == True:
                            SESSION["grille"][h][l-1] = False
                            l=l-1
                            nb_provisoir-=1 
                    if l-1<0 or SESSION["grille"][h][l-1] == False:        
                        if gauche not in memoire_direction:
                            memoire_direction.append(gauche)
            if  len (memoire_direction)>=4:
                nb=0
            else:
                nb=nb_provisoir        
    
    SESSION["bool_grille"]=True
        
  

        
        
         

"""
Vérification pour mise en session des choix de la joueuse 
print ("affichage de la session choix ")
for i in range (len(SESSION["choix"])):
    print ("affichage de la session choix")
    print (SESSION["choix"][i])
"""

   
    
    





