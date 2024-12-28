import re
from collections import deque
from module_perso.pion import Pion


class Joueur:
    Joueurs_instance = 1  # Variable globale pour suivre l'ID du joueur en cours.
    Joueurs_pseudos_uniques = (
        set()
    )  # Variable globale pour stocker les pseudos uniques.

    def __init__(self):
        self.__id = Joueur.Joueurs_instance
        Joueur.Joueurs_instance += 1
        self.__pseudo = self.__demander_pseudo()
        self.__scores = deque()  # Historique des scores
        self.__victoires_consecutives = 0
        self.pion = Pion(self.__pseudo)  # chaque joueur a son propre pion

    def __demander_pseudo(self):
        while True:
            pseudo = input(
                f"Joueur {self.__id}, entrez votre pseudo UNIQUE (3-15 caractères, lettres, chiffres, '_' ou '-'):"
            )
            if (
                not re.match(r"^[a-zA-Z0-9_\-]{3,15}$", pseudo)
                or pseudo in Joueur.Joueurs_pseudos_uniques
            ):
                print("Pseudo invalide. Veuillez respecter les règles !")
                continue
            print(f"Pseudo '{pseudo}' validé !")
            Joueur.Joueurs_pseudos_uniques.add(pseudo)
            return pseudo

    @property
    def pseudo(self):
        return self.__pseudo

    def ajouter_victoire(self):
        score = 1
        if self.__victoires_consecutives >= 3:
            score += 1  # +1 bonus si série de victoires consécutives
        self.__scores.append(score)
        self.__victoires_consecutives += 1

    def quitter(self):
        self.__victoires_consecutives = 0

    def get_scores(self):
        return sorted(self.__scores, reverse=True)

    def scores_detail(self):
        for score in self.__scores:
            yield score

    def calculer_score_total(self):
        return sum(map(lambda x: x, self.__scores))

    def __str__(self):
        return f"Joueur {self.__id}: {self.__pseudo}, Score total: {self.calculer_score_total()}, {self.pion}"

    def __eq__(self, other):
        return isinstance(other, Joueur) and self.__pseudo == other.pseudo

    def __lt__(self, other):
        return self.calculer_score_total() < other.calculer_score_total()

    @staticmethod
    def meilleurs_scores(joueurs):
        return sorted(
            joueurs, key=lambda joueur: joueur.calculer_score_total(), reverse=True
        )
