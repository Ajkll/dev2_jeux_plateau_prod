import random
from module_perso.pion import Pion
from module_perso.decorateurs import log_result
import re


class Jeu:
    def __init__(self, nom_joueurs, plateau=None):
        self.plateau = plateau
        self.pions = [Pion(nom) for nom in nom_joueurs]
        self.joueur_actuel = 0
        self.case_victoire = (
            self.plateau.taille - 1
        )  # Automatique avec la taille du plateau.
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
        self.compteur_cascade = 0
        self.limite_cascade = 5

    def lancer_de(self):
        return random.randint(1, 6)

    def avancer_pion(self, pion, valeur):
        self.compteur_cascade = 0
        return self._gerer_deplacement(pion, valeur)

    def reculer_pion(self, pion, valeur):
        return self._gerer_deplacement(pion, -valeur)

    @log_result
    def _gerer_deplacement(self, pion, valeur):
        while self.compteur_cascade < self.limite_cascade:
            pion.deplacer(valeur)
            effet = self.plateau.obtenir_effet_case(pion.position)
            self.compteur_cascade += 1
            if effet:
                return effet
            else:
                break
        return None

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
