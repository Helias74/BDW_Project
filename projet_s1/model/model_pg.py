import psycopg
from psycopg import sql
from logzero import logger

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


def top5_couleurs(connexion):
    """
    Retourne le top 5 des couleurs les plus fréquentes dans la table 'piece'.
    """
    # Requête SQL pour obtenir les couleurs les plus fréquentes
    query = sql.SQL("""
        SELECT couleur, COUNT(*) AS nombre_pieces
        FROM piece
        GROUP BY couleur
        ORDER BY nombre_pieces DESC
        LIMIT 5;
    """)
    
    return execute_select_query(connexion, query)

def score_min_max(connexion):
    """
    Retourne pour chaque joueuse son score min et max 
    """
    # Requête SQL 
    query = sql.SQL("""
        SELECT 
        JOUEUSE.Prenom,
        JOUEUSE.Date_d_inscription,
        MIN(PARTICIPATION.Score) AS Score_Minimal,
        MAX(PARTICIPATION.Score) AS Score_Maximal
        FROM 
        JOUEUSE
        JOIN 
        PARTICIPATION ON JOUEUSE.Prenom = PARTICIPATION.Prenom 
        AND JOUEUSE.Date_d_inscription = PARTICIPATION.Date_d_inscription
        GROUP BY 
        JOUEUSE.Prenom, 
        JOUEUSE.Date_d_inscription;
    """)
    
    return execute_select_query(connexion, query)

def min_max_defausse(connexion):
    """
    partie avec le moins et le plus de pièce déffausé 
    """
    query = sql.SQL("""
    SELECT 
        tour_id, 
        COUNT(*) AS nb_pieces_defaussees
    FROM 
        enregistre
    WHERE 
        action = 'défausser'
    GROUP BY 
        tour_id
    ORDER BY 
        nb_pieces_defaussees ASC;
    LIMIT 1;
    """)

def min_max_pioche(connexion):
    """
    partie avec le moins et le plus de pièce pioché 
    """
    query = sql.SQL("""
    SELECT 
        tour_id, 
        COUNT(*) AS nb_pieces_piochees
    FROM 
        enregistre
    WHERE 
        action = 'piocher'
    GROUP BY 
        tour_id
    ORDER BY 
        nb_pieces_piochees ASC;
    """)


def get_briques_pour_pioche(connexion):
    query = sql.SQL("""
        SELECT *
        FROM piece
        WHERE longueur <= 2 OR largeur <= 2
        ORDER BY RANDOM()
        LIMIT 4;
    """)
    return execute_select_query(connexion, query)
    