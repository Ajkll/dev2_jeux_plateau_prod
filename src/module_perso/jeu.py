import random
import re
from module_perso.pion import Pion
from module_perso.decorateurs import log_result
from module_perso.fraction import Fraction
from module_perso.logging_config import get_logger

logger = get_logger(__name__)


class ExceptionCritiqueTourSuivant(Exception):
    pass


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
        self.ajouter_questions_fraction(nombre_questions=14)
        self.generateur_questions = self.generer_questions()

    def lancer_de(self):
        """lancer un de pour determniner la valeur du deplacement du joueur initiateur!"""
        return random.randint(1, 6)

    def avancer_pion(self, pion, valeur):
        """avancer le pion de 'valeur' case"""
        self.compteur_cascade = 0
        return self._gerer_deplacement(pion, valeur)

    def reculer_pion(self, pion, valeur):
        """reculer le pion de 'valeur' case"""
        return self._gerer_deplacement(pion, -valeur)

    @log_result
    def _gerer_deplacement(self, pion, valeur):
        """gerer le deplacement du pion et l'effet de la case speciale en cascade limiter a une suite d'evenment en chaine de 5 max"""
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
        """Poser une question et retourner la question posée pour les joueurs qui sont tomber sur une cases speciale question"""
        try:
            return next(self.generateur_questions)
        except StopIteration:
            print(
                "Toutes les questions ont été posées. Génération de nouvelles questions..."
            )
            self.ajouter_questions_fraction(
                nombre_questions=10
            )  # Génère 10 nouvelles questions si on tombe en rabe
            self.generateur_questions = (
                self.generer_questions()
            )  # Réinitialise le générateur avec ces nouvelles questions
            return next(
                self.generateur_questions
            )  # Retourne la première question du nouveau lots de questions

    def generer_questions(self):
        """Génére des questions et les retourne un par un plus performant que sans générateur"""
        for question in self.questions:
            yield question

    def verifier_reponse(self, reponse, question):
        """verifie si la reponse est correcte pour un evenement de cases special question"""
        if not re.match(r"^\d+$", str(reponse)):
            print("Réponse invalide. Veuillez entrer un nombre.")
            return False
        return int(reponse) == question["reponse"]

    def est_vainqueur(self, pion):
        """Verifie si le pion est au dessus de la case de victoire"""
        try:
            return pion.position >= self.case_victoire
        except Exception as e:
            logger.exception(
                f"Une erreur s'est produite lors de la verification du vainqueur : {e}"
            )
            exit(
                -1
            )  # le programme dois s'arreter si cela arrive sans sauvegarder le score dans la db donc !

    def tour_suivant(self):
        """Passe au joueur suivant"""
        try:
            self.joueur_actuel = (self.joueur_actuel + 1) % len(self.pions)
        except ExceptionCritiqueTourSuivant:
            logger.exception(
                "Le joueur actuel n'a pas pu passer au tour suivant erreur critique"
            )
            exit(-1)  # le programme dois s'arreter si cela arrive

    def ajouter_questions_fraction(self, nombre_questions=5):
        """genere avec la class fonction des questions de calculs de fractions"""
        for _ in range(nombre_questions):
            # deux fractions random
            num1, den1 = random.randint(1, 10), random.randint(1, 10)
            num2, den2 = random.randint(1, 10), random.randint(1, 10)
            frac1, frac2 = Fraction(num1, den1), Fraction(num2, den2)

            operation = random.choice(["+", "-", "*"])
            resultat = {
                "+": frac1 + frac2,
                "-": frac1 - frac2,
                "*": frac1 * frac2,
            }[operation]
            question_texte = {
                "+": f"Quelle est la somme de {frac1} et {frac2} ?",
                "-": f"Quelle est la différence entre {frac1} et {frac2} ?",
                "*": f"Quel est le produit de {frac1} et {frac2} ?",
            }[operation]

            # Génération des options
            options = [
                str(resultat),
                str(resultat + Fraction(random.randint(1, 5), random.randint(1, 5))),
                str(resultat - Fraction(random.randint(1, 5), random.randint(1, 5))),
            ]
            random.shuffle(options)
            reponse_index = options.index(str(resultat)) + 1

            self.questions.append(
                {
                    "question": question_texte,
                    "options": [f"{i+1}. {opt}" for i, opt in enumerate(options)],
                    "reponse": reponse_index,
                }
            )
