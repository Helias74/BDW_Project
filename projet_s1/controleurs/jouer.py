import psycopg
from model.model_pg import get_briques_pour_pioche

res = get_briques_pour_pioche(SESSION["CONNEXION"])
if res is not None:
                SESSION["pioche"] = res
else:
    SESSION["pioche"] = "Pas suffisament de brique disponible et compatible pour former la pioche."
    



print(GET["brique_id"][0])




