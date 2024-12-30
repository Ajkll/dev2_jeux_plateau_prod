from module_perso.plateau import Plateau
import random
from module_perso.logging_config import get_logger

logger = get_logger(__name__)


class ExceptionCustomGenerationCritiqueErreur(Exception):
    pass


class Changement_map:
    @staticmethod
    def appliquer_changement(jeu, joueurs):
        try:
            # Créer un nouveau plateau
            taille_plateau = random.randint(10, 15)
            cases_speciales = Plateau.generer_cases_speciales(
                taille_plateau, ["reculer", "question", "changement_map"]
            )
            nouveau_plateau = Plateau(
                taille=taille_plateau, cases_speciales=cases_speciales
            )

            # Réinitialiser les propriétés du jeu liées au plateau
            jeu.plateau = nouveau_plateau
            jeu.case_victoire = (
                nouveau_plateau.taille - 1
            )  # Déjà géré par le nouveau plateau.

            # Réinitialiser la position des pions des joueurs
            for joueur in joueurs:
                joueur.pion.reset()

            print("Changement de map effectué : Nouvelle taille", taille_plateau - 1)

        except ExceptionCustomGenerationCritiqueErreur as e:
            logger.exception(
                f"Une erreur s'est produite lors du changement de map : {e}"
            )
            exit(-1)  # le programme dois s'arreter si cela arrive
