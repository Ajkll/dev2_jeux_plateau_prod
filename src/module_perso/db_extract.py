import psycopg2
from datetime import datetime


def obtenir_connexion():
    return psycopg2.connect(
        dbname="jeu_scores", user="postgres", password="postgres", host="db", port=5432
    )


def enregistrer_scores(joueurs):
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
        print("Scores enregistrés avec succès dans la base de données.")
    except psycopg2.Error as e:
        print(f"Erreur lors de l'insertion dans la base de données : {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def recuperer_scores():

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
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()


def top_3(scores):

    scores_aggreges = {}
    for score_dict in scores:
        for nom, score in score_dict.items():
            scores_aggreges[nom] = scores_aggreges.get(nom, 0) + score

    scores_tries = sorted(scores_aggreges.items(), key=lambda x: x[1], reverse=True)

    # le top 3 seulement
    return scores_tries[:3]
