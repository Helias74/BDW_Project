import psycopg
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
            SESSION["choix"].append(SESSION["pioche"][i])
            res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            while res3 in SESSION["choix"]:
                res3 = get_briques_pour_pioche_maj(SESSION["CONNEXION"])
            SESSION["pioche"][i]=res3[0]

        

    





