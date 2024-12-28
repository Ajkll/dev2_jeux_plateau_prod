import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from module_perso.jeu import Jeu
from module_perso.affichage import Affichage
from module_perso.logging_config import get_logger
from module_perso.joueur import Joueur
from module_perso.plateau import Plateau
from module_perso.db_extract import enregistrer_scores, recuperer_scores

logger = get_logger(__name__)


def traiter_case_speciale(effet, jeu, affichage, pion_actuel):
    if effet == "reculer":
        affichage.affichage_effet_case(effet, pion_actuel)
        jeu.reculer_pion(pion_actuel, 2)
    elif effet == "question":
        affichage.affichage_effet_case(effet, pion_actuel)
        question = jeu.poser_question()
        reponse = affichage.poser_question(question)
        correct = jeu.verifier_reponse(reponse, question)
        affichage.affichage_resultat_question(correct, pion_actuel)
        if correct:
            jeu.avancer_pion(pion_actuel, 1)
        else:
            jeu.reculer_pion(pion_actuel, 1)
    elif effet == "changement_map":
        affichage.affichage_effet_case(effet, pion_actuel)
        affichage.affichage_plateau(jeu.plateau)


def top_3(scores):

    scores_aggreges = {}
    for score_dict in scores:
        for nom, score in score_dict.items():
            scores_aggreges[nom] = scores_aggreges.get(nom, 0) + score

    scores_tries = sorted(scores_aggreges.items(), key=lambda x: x[1], reverse=True)

    # le top 3 seulement
    return scores_tries[:3]


def main():
    print(f"Top 3 : { top_3(recuperer_scores()) }")
    logger.info("Lancement du jeu de plateau.")
    affichage = Affichage()

    nb_joueurs = 2  # Nombre de joueurs.
    joueurs = [Joueur() for _ in range(nb_joueurs)]

    # Paramètres du plateau
    taille_plateau = 12
    effets_possibles = ["reculer", "question", "changement_map"]

    while True:  # Boucle de jeu principale.
        # Initialisation du plateau et du jeu
        cases_speciales = Plateau.generer_cases_speciales(
            taille_plateau, effets_possibles
        )
        plateau = Plateau(taille=taille_plateau, cases_speciales=cases_speciales)
        jeu = Jeu([joueur.pseudo for joueur in joueurs], plateau=plateau)
        logger.info("Nouvelle partie initialisée.")
        affichage.afficher_message("Démarrage du jeu de plateau !")
        affichage.affichage_plateau(jeu.plateau)

        vainqueur = False
        while not vainqueur:
            joueur_actuel = joueurs[jeu.joueur_actuel]
            pion_actuel = joueur_actuel.pion

            choix_action = affichage.demander_action(pion_actuel)

            if choix_action in {"q", "esc"}:
                logger.warning("Le joueur a stoppé la session")
                affichage.afficher_message("Arrêt du jeu demandé. Arrêt en cours.")
                enregistrer_scores(joueurs)
                joueur_actuel.quitter()
                return  # Quitte le jeu.

            elif choix_action == "n":
                jeu.tour_suivant()
                affichage.afficher_message(f"{pion_actuel.nom} a passé son tour.")

            elif choix_action == "y":
                valeur_de = jeu.lancer_de()
                affichage.afficher_message(
                    f"{pion_actuel.nom} a lancé le dé et a obtenu un {valeur_de}."
                )

                effet = jeu.avancer_pion(pion_actuel, valeur_de)
                affichage.affichage_pion(pion_actuel)

                if effet:
                    traiter_case_speciale(effet, jeu, affichage, pion_actuel)

                if jeu.est_vainqueur(pion_actuel):
                    affichage.annoncer_vainqueur(pion_actuel)
                    joueur_actuel.ajouter_victoire()
                    vainqueur = True
                else:
                    jeu.tour_suivant()

        # Afficher les scores après chaque partie.
        affichage.afficher_message("Score :")
        for joueur in joueurs:
            affichage.afficher_message(str(joueur))

        # Afficher le meilleur joueur.
        meilleur = max(joueurs, key=lambda joueur: joueur.calculer_score_total())
        affichage.afficher_message(f"Joueur gagnant actuellement: {meilleur}")

        # Demander si on rejoue.
        choix_rejouer = affichage.demander_rejouer()
        logger.info(f"Choix de rejouer : {choix_rejouer}")
        if choix_rejouer == "n":
            affichage.afficher_message("Scores finaux :")
            joueurs_tries = Joueur.meilleurs_scores(joueurs)
            for joueur in joueurs_tries:
                affichage.afficher_message(str(joueur))
            enregistrer_scores(joueurs)
            affichage.afficher_message("Merci d'avoir joué !")
            logger.info("Fermeture du jeu.")
            break  # Quitter le jeu.
            # Réinitialisez les positions des pions.
        else:
            for joueur in joueurs:
                joueur.pion.reset()


if __name__ == "__main__":
    main()
