import psycopg
import random
from datetime import datetime
from model.model_pg import (
    get_briques_pour_pioche,
    get_briques_pour_pioche_maj,
    get_briques_pour_pioche_hard,
    get_briques_pour_pioche_maj_hard,
    get_joueuses,
    insert_joueuse,
    get_joueuse_by_name,
    insert_tour,
    insert_partie,
    insert_participation,
)
###Pour la gestion de lancement de la partie 
if "longueur_grille" in GET and "hauteur_grille" in GET:
    SESSION["partie_debut"] = True
    SESSION["Date_deb"] = datetime.today().date()

###Pour gérer la fin de partie 

if "quitter" in GET:
    if GET["quitter"][0] == "confirmer":
        SESSION["avancement_tours"]=0
        SESSION["nb_tours"] = 1
        SESSION["scores"] = {joueuse_id: 0 for joueuse_id in SESSION["tab_joueuse"]} #rermise des score à 0
        SESSION["Date_fin"] = datetime.today().date()
        insert_partie(SESSION["CONNEXION"], SESSION["Date_deb"], SESSION["Date_fin"])
        
        SESSION["partie_debut"] = False
        
        
###Pour récupérer le mode
if "mode" in GET:
    SESSION["mode"] = int (GET["mode"][0])
    print (SESSION["mode"])
    
 
###Pour récupérer la liste des joueuses
res_joueuse = get_joueuses(SESSION["CONNEXION"])
if res_joueuse is not None:
    SESSION["joueuses"] = res_joueuse
else:
    SESSION["joueuses"] = "Aucune joueuses n'est enregistrés "

###Pour récupérer la liste des joueuses choisies pour la partie 
if "joueuses" in GET:
    for i in  GET["joueuses"]:
        SESSION["tab_joueuse"].append(i)
        print (i)
    SESSION["joueuse_actuelle"]=SESSION["tab_joueuse"][0]
    SESSION["scores"] = {joueuse_id: 0 for joueuse_id in SESSION["tab_joueuse"]}


###Pour ajouter une joueuse

if POST and 'prenom' in POST and 'date_inscription' in POST:  # formulaire soumis avec les champs nécessaires
    prenom = POST['prenom'][0]  # Récupérer le prénom
    date_inscription = POST['date_inscription'][0]  # Récupérer la date d'inscription
    avatar = POST['avatar'][0] if 'avatar' in POST else None  # Si l'Avatard est male renseigné

    try:
        result = insert_joueuse(SESSION['CONNEXION'], prenom, date_inscription, avatar)
        if result:
            REQUEST_VARS['message'] = f"La joueuse {prenom} a été ajoutée avec succès."
            REQUEST_VARS['message_class'] = "alert-success"
        else:
            REQUEST_VARS['message'] = f"Erreur lors de l'ajout de la joueuse {prenom}."
            REQUEST_VARS['message_class'] = "alert-error"
    except Exception as e:
        REQUEST_VARS['message'] = f"Erreur technique : {e}"
        REQUEST_VARS['message_class'] = "alert-error"




         


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
    if SESSION["longueur"] != int(GET["longueur_grille"][0]) or SESSION["hauteur"] != int(GET["hauteur_grille"][0]):
        SESSION["bool_grille"]=False
    if SESSION["bool_grille"]==False:
        SESSION["longueur"] = int(GET["longueur_grille"][0])
        SESSION["hauteur"] = int(GET["hauteur_grille"][0])
        SESSION["grille"] = [[SESSION["case"] for _ in range(SESSION["longueur"])] for _ in range(SESSION["hauteur"])]
        SESSION["grille_piece"] = [[(SESSION["case"],"#0D97D7") for _ in range(SESSION["longueur"])] for _ in range(SESSION["hauteur"])]
        for i in range  (SESSION["hauteur"]):
            for j in range (SESSION["longueur"]):
                SESSION["grille"][i][j]=SESSION["case"]
                SESSION["grille_piece"][i][j]=(SESSION["case"],"#0D97D7")
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
        
        for i in range  (SESSION["hauteur"]):
            for j in range (SESSION["longueur"]):
                if SESSION["grille"][i][j]==SESSION["case"]:
                    SESSION["grille_piece"][i][j]=(SESSION["case"],"#0D97D7")        
                if SESSION["grille"][i][j]==SESSION["cible"]:
                    SESSION["grille_piece"][i][j]=(SESSION["cible"],"#FBFF26")  
    SESSION["bool_grille"]=True
        
  
####GESTION DES PLACEMENTS SUR LA GRILLE 


###Pour la gestion de la pioche 

if SESSION["pioche"] is None:
    if SESSION["mode"]==1:
        res = get_briques_pour_pioche(SESSION["CONNEXION"])
    else:
        res = get_briques_pour_pioche_hard(SESSION["CONNEXION"])
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
            if SESSION["mode"]==1:
                res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            else:
                res3 = get_briques_pour_pioche_maj_hard(SESSION["CONNEXION"])
            while res3 in SESSION["choix"]:
                if SESSION["mode"]==1:
                    res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
                else:
                    res3 = get_briques_pour_pioche_maj_hard(SESSION["CONNEXION"])
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
    if (SESSION["longeur_brique_select"] + SESSION["posx"]) <=SESSION["hauteur"]-1 and (SESSION["largeur_brique_select"] + SESSION["posx"]) <=SESSION["longueur"]-1 :
        b=True
        for i in range (SESSION["longeur_brique_select"]):
            for j in range(SESSION["largeur_brique_select"]):
                if SESSION["grille"][SESSION["posx"]+i][SESSION["posy"]+j]!=SESSION["cible"]:
                    print ("test de la validité du placement ")
                    b=False
        #Changement de tours et placement 
    else:
        b=False
        
    if b==False:
        print ("Aucune piece n'a été placé")
    else:
        for i in range (SESSION["longeur_brique_select"]):
            for j in range(SESSION["largeur_brique_select"]):
                SESSION["grille"][SESSION["posx"]+i][SESSION["posy"]+j] = SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][0]
                SESSION["couleur"] = SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][4]
                SESSION["grille_piece"][SESSION["posx"]+i][SESSION["posy"]+j]  =  (SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][0],SESSION["couleur"])
        print ("une piece a été placé")
        ###Pour Actuamisation et avncement du tours
    #print ("le tableau tab joueuse est print en dessous")
    #print (SESSION["tab_joueuse"])
    
    if SESSION["tab_joueuse"]:
        ###Gestion des infos sur les tours :
        ##Pour table tours
        print ("impréssion des scores")
        print (SESSION["scores"])
        if SESSION["posx"]<21:
            insert_tour(SESSION["CONNEXION"], 'ajouter', SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][0], SESSION["tab_joueuse"][SESSION["avancement_tours"]])
        else:
            insert_tour(SESSION["CONNEXION"], 'defausser', SESSION["choix_ensemble"][len(SESSION["choix_ensemble"])-1][0], SESSION["tab_joueuse"][SESSION["avancement_tours"]])
            SESSION["scores"][SESSION["tab_joueuse"][SESSION["avancement_tours"]]] += 2
        
        SESSION["avancement_tours"] += 1
        if SESSION["avancement_tours"] >= len(SESSION["tab_joueuse"]):  # Si on dépasse la dernière joueuse
            SESSION["avancement_tours"] = 0  # Revenir à la première joueuse
            SESSION["nb_tours"] += 1  # Compter un tour supplémentaire
        SESSION["joueuse_actuelle"] = SESSION["tab_joueuse"][SESSION["avancement_tours"]]
        
        ###Pour gestion du gagnant
        
        gagnant = SESSION["tab_joueuse"][0][0]  # ID de la première joueuse
        score_gagnant = SESSION["scores"].get(SESSION["tab_joueuse"][0][0], 0)  # Score de la première joueuse

        for i in SESSION["tab_joueuse"]:  # Parcours de toutes les joueuses
            joueuse_id = i[0]  # Récupère l'ID de la joueuse première pour commencer 
            joueuse_score = SESSION["scores"].get(joueuse_id, 0)  # Récupère son score (0 par défaut)
    
            if joueuse_score < score_gagnant:  # changement de gagnant 
                print("Changement de vainqueur")
                score_gagnant = joueuse_score  # Met à jour le score gagnant
                SESSION["gagnant"] = joueuse_id  # Met à jour l'ID du gagnant
            if joueuse_id==SESSION["gagnant"]:
                insert_participation(SESSION["CONNEXION"], SESSION["Date_deb"], joueuse_id, joueuse_score, Est_Gagnante=True)
            else:
                insert_participation(SESSION["CONNEXION"], SESSION["Date_deb"], joueuse_id, joueuse_score, Est_Gagnante=False)
    
        
            
    
        





   
    
    





