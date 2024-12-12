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
    Retourne pour chaque joueuse son score min et max.
    Trop d'instance inutile renvoyé (fonctionnel)
    """
    # Requête SQL
    query = sql.SQL("""
        SELECT 
            joueuse.id AS Joueuse_ID,
            joueuse.Prenom,
            joueuse.Date_d_inscription,
            MIN(participation.Score) AS Score_Minimal,
            MAX(participation.Score) AS Score_Maximal
        FROM 
            joueuse
        JOIN 
            participation ON joueuse.id = participation.Joueuse_id
        GROUP BY 
            joueuse.id, 
            joueuse.Prenom, 
            joueuse.Date_d_inscription;
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

def get_briques_pour_pioche_maj(connexion):
    query = sql.SQL("""
        SELECT *
        FROM piece
        WHERE longueur <= 2 OR largeur <= 2
        ORDER BY RANDOM()
        LIMIT 1;
    """)
    return execute_select_query(connexion, query)



def get_briques_pour_pioche_hard(connexion):
    query = sql.SQL("""
        SELECT *
        FROM piece
        ORDER BY RANDOM()
        LIMIT 4;
    """)
    return execute_select_query(connexion, query)

def get_briques_pour_pioche_maj_hard(connexion):
    query = sql.SQL("""
        SELECT *
        FROM piece
        ORDER BY RANDOM()
        LIMIT 1;
    """)
    return execute_select_query(connexion, query)


def get_joueuses(connexion):
    query = sql.SQL("""
        SELECT * FROM joueuse;
    """)
    return execute_select_query(connexion, query)



def insert_joueuse(connexion, Prenom, Date_d_inscription, Avatar):
    """
    Insère une joueuse dans la base de données.
    """
    query = '''
        INSERT INTO joueuse (Prenom, Date_d_inscription, Avatar)
        VALUES (%s, %s, %s)
    '''
    return execute_other_query(connexion, query, [Prenom,Date_d_inscription,Avatar])

def get_joueuse_by_name(connexion, prenom):
    """
    Récupère les joueuses avec un prénom donné.
    """
    query = '''
        SELECT * FROM joueuse WHERE Prenom = %s
    '''
    return execute_select_query(connexion, query, [prenom])


def insert_tour(connexion, action, piece_id, joueuse_id):
    """
    Insère un tour dans la table 'tours'.
    """
    query = '''
        INSERT INTO tours (action, piece_id, joueuse_id)
        VALUES (%s, %s, %s)
    '''
    return execute_other_query(connexion, query, [action, piece_id, joueuse_id])


def insert_partie(connexion, Date_deb, Date_fin=None):
    """
    Insère une partie dans la base de données.
    """
    query = '''
        INSERT INTO partie (Date_deb, Date_fin)
        VALUES (%s, %s)
    '''
    return execute_other_query(connexion, query, [Date_deb, Date_fin])


def insert_participation(connexion, Date_deb, Joueuse_id, Score, Est_Gagnante=False):
    """
    Insère une participation dans la table participation.
    """
    query = '''
        INSERT INTO participation (Date_deb, Joueuse_id, Score, Est_Gagnante)
        VALUES (%s, %s, %s, %s)
    '''
    return execute_other_query(connexion, query, [Date_deb, Joueuse_id, Score, Est_Gagnante])