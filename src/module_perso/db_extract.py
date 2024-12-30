import psycopg2
from datetime import datetime
from module_perso.logging_config import get_logger

logger = get_logger(__name__)


class DBerrorManipulation(Exception):
    pass


def obtenir_connexion():
    """Obtenir une connexion à la base de données PostgreSQL tournant sur le docker au port 5432"""
    try:
        return psycopg2.connect(
            dbname="jeu_scores",
            user="postgres",
            password="postgres",
            host="db",
            port=5432,
        )
    except psycopg2.OperationalError as e:
        logger.exception(
            f"Une erreur s'est produite lors de la connexion à la base de données : {e}"
        )


def enregistrer_scores(joueurs):
    """Enregistrer les scores des joueurs dans la base de données"""
    try:
        conn = obtenir_connexion()
        cursor = conn.cursor()

        # Insérer les scores des joueurs
        for joueur in joueurs:
            cursor.execute(
                """
                INSERT INTO scores (pseudo, score_total, date_partie)
                VALUES (%s, %s, %s);
            """,
                (joueur.pseudo, joueur.calculer_score_total(), datetime.now()),
            )

        # Valider la modifiaction en db
        conn.commit()
        logger.info("Scores enregistrés avec succès dans la base de données.")
        print("Scores enregistrés avec succès dans la base de données.")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")
        logger.error(f"Erreur lors de l'insertion dans la base de données : {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def recuperer_scores():
    """Récupérer les scores des joueurs depuis la base de données."""

    try:
        conn = obtenir_connexion()
        cursor = conn.cursor()

        # Récupérer tous les scores
        cursor.execute(
            """
            SELECT pseudo, score_total
            FROM scores
            ORDER BY score_total DESC;
        """
        )
        rows = cursor.fetchall()

        scores_tries = [{row[0]: row[1]} for row in rows]
        return scores_tries
    except psycopg2.Error as e:
        print(f"Erreur lors de la récupération des scores : {e}")
        logger.error(f"Erreur lors de la sélection des scores : {e}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()


def top_3(scores):
    """function pour obtenir les meilleurs scores (top3) parmit tout les joueur dans la base de données"""
    try:
        scores_aggreges = {}
        for score_dict in scores:
            for nom, score in score_dict.items():
                scores_aggreges[nom] = scores_aggreges.get(nom, 0) + score

        scores_tries = sorted(scores_aggreges.items(), key=lambda x: x[1], reverse=True)

        # le top 3 seulement
        return scores_tries[:3]

    except DBerrorManipulation as e:
        logger.error(
            f"Erreur lors de la sélection des meilleurs scores  dans la db: {e}"
        )
