import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from module_perso.jeu import Jeu
from module_perso.affichage import Affichage
from module_perso.logging_config import get_logger

logger = get_logger(__name__)


def main():
    logger.info("Lancement du jeu de plateau.")
    affichage = Affichage()

    # Initialisation initiale
    noms_joueurs = ["Pion 1", "Pion 2"]
    cases_speciales = {5: "reculer", 8: "question", 10: "changement_map"}
    logger.debug(
        f"Noms des joueurs: {noms_joueurs}, Cases spéciales: {cases_speciales}"
    )

    while True:
        # Réinitialisation pour une nouvelle partie
        jeu = Jeu(noms_joueurs, taille_plateau=12, cases_speciales=cases_speciales)
        logger.info("Nouvelle partie initialisée.")
        affichage.afficher_message("Démarrage du jeu de plateau !")
        affichage.affichage_plateau(jeu.plateau)

        vainqueur = False
        while not vainqueur:
            pion_actuel = jeu.pions[jeu.joueur_actuel]
            logger.debug(f"Tour du joueur: {pion_actuel.nom}")

            choix_action = affichage.demander_action(pion_actuel)
            logger.info(f"Action choisie par {pion_actuel.nom}: {choix_action}")

            if choix_action == "q" or choix_action == "esc":
                logger.warning("Arrêt du jeu demandé par le joueur.")
                affichage.afficher_message(
                    "Arrêt du jeu demandé. Arrêt du Docker en cours."
                )
                return  # Quitte complètement le jeu

            if choix_action == "y":
                valeur_de = jeu.lancer_de()
                logger.info(f"{pion_actuel.nom} a lancé un {valeur_de}.")
                affichage.afficher_message(
                    f"{pion_actuel.nom} a lancé le dé et a obtenu un {valeur_de}."
                )

                effet = jeu.avancer_pion(pion_actuel, valeur_de)
                logger.debug(f"Effet de la case: {effet}")
                affichage.affichage_pion(pion_actuel)

                if effet == "reculer":
                    affichage.affichage_effet_case(effet, pion_actuel)
                    jeu.reculer_pion(pion_actuel, 2)
                    logger.info(f"{pion_actuel.nom} recule de 2 cases.")

                elif effet == "question":
                    affichage.affichage_effet_case(effet, pion_actuel)
                    question = jeu.poser_question()
                    logger.debug(f"Question posée: {question['question']}")
                    reponse = affichage.poser_question(question)
                    correct = jeu.verifier_reponse(reponse, question)
                    logger.info(
                        f"Réponse donnée: {reponse}, Correct: {'Oui' if correct else 'Non'}"
                    )
                    affichage.affichage_resultat_question(correct, pion_actuel)
                    if correct:
                        jeu.avancer_pion(pion_actuel, 1)
                        logger.info(f"{pion_actuel.nom} avance de 1 case.")
                    else:
                        jeu.reculer_pion(pion_actuel, 1)
                        logger.info(f"{pion_actuel.nom} recule de 1 case.")

                elif effet == "changement_map":
                    affichage.affichage_effet_case(effet, pion_actuel)
                    affichage.affichage_plateau(jeu.plateau)
                    logger.info(f"Changement de plateau pour {pion_actuel.nom}.")

                if jeu.est_vainqueur(pion_actuel):
                    affichage.annoncer_vainqueur(pion_actuel)
                    logger.info(f"{pion_actuel.nom} a gagné la partie !")
                    vainqueur = True
                else:
                    jeu.tour_suivant()
                    logger.debug(f"Passage au joueur suivant: {jeu.joueur_actuel}")

        # Demander si les joueurs veulent rejouer
        choix_rejouer = affichage.demander_rejouer()
        logger.info(f"Choix de rejouer: {choix_rejouer}")
        if choix_rejouer == "n":
            affichage.afficher_message("Fin du jeu. Merci d'avoir joué !")
            logger.info("Fin de la session de jeu.")
            break  # Fin du jeu, sortir de la boucle principale


if __name__ == "__main__":
    main()
