import random
from module_perso.pion import Pion
from module_perso.plateau import Plateau
from module_perso.changement_map import Changement_map
from module_perso.decorateurs import log_result
import re


class Jeu:
    def __init__(
        self, nom_joueurs, plateau=None, taille_plateau=10, cases_speciales=None
    ):
        self.plateau = plateau if plateau else Plateau(taille_plateau, cases_speciales)
        self.pions = [Pion(nom) for nom in nom_joueurs]
        self.joueur_actuel = 0
        self.case_victoire = (
            self.plateau.taille - 1
        )  # Utilise la taille du plateau pour la case victoire.
        self.changement_map = Changement_map(
            taille_nouvelle_map=15, cases_speciales=cases_speciales
        )
        self.questions = [
            {
                "question": "Quelle est la capitale de la Belgique ?",
                "options": ["1. Bruxelles", "2. Londres", "3. Berlin"],
                "reponse": 1,
            },
            {
                "question": "Combien font 6 x 6 ?",
                "options": ["1. 6", "2. 36", "3. 12"],
                "reponse": 2,
            },
            {
                "question": "Comment s'appelle le local TI ?",
                "options": ["1. openLab", "2. L221", "3. Ephec Ti"],
                "reponse": 1,
            },
        ]

    @log_result
    def lancer_de(self):
        return random.randint(1, 6)

    def avancer_pion(self, pion, valeur):
        pion.deplacer(valeur)
        effet = self.plateau.obtenir_effet_case(pion.position)

        if effet == "changement_map":
            self.changement_map.appliquer_changement(self)

        return effet

    def reculer_pion(self, pion, valeur):
        pion.reculer(valeur)

    def poser_question(self):
        question_gen = self.generer_questions()
        return next(question_gen)

    def generer_questions(self):
        for question in self.questions:
            yield question

    def verifier_reponse(self, reponse, question):
        if not re.match(r"^\d+$", str(reponse)):
            print("Réponse invalide. Veuillez entrer un nombre.")
            return False
        return int(reponse) == question["reponse"]

    def est_vainqueur(self, pion):
        return pion.position >= self.case_victoire

    def tour_suivant(self):
        self.joueur_actuel = (self.joueur_actuel + 1) % len(self.pions)
