import re
from collections import deque
from module_perso.pion import Pion
from module_perso.decorateurs import log_result


class Joueur:
    Joueurs_instance = 1  # Variable globale pour suivre l'ID du joueur en cours.
    Joueurs_pseudos_uniques = (
        set()
    )  # Variable globale pour stocker les pseudos uniques.

    def __init__(self, pseudo_proposer=None):
        self.__id = Joueur.Joueurs_instance
        Joueur.Joueurs_instance += 1
        self.__pseudo = self.__demander_pseudo(pseudo_proposer)
        self.__scores = deque()  # Historique des scores
        self.__victoires_consecutives = 0
        self.pion = Pion(self.__pseudo)  # chaque joueur a son propre pion

    @log_result
    def __demander_pseudo(self, pseudo_proposer):
        """Methode pour valider les pseudo choisie cotés clients"""
        if pseudo_proposer and re.match(
            r"^[a-zA-Z0-9_\-]{3,15}$", pseudo_proposer
        ):  # si les pseudo proposer ne match pas alors on leur donne un pseudo generique !
            if pseudo_proposer not in Joueur.Joueurs_pseudos_uniques:
                Joueur.Joueurs_pseudos_uniques.add(pseudo_proposer)
                print(f"votre pseudo : '{pseudo_proposer}' est valider !")
                return pseudo_proposer
            else:
                print(
                    f"malheureusement le pseudo '{pseudo_proposer}' est deja utiliser ! vous aurez donc un pseudo generique"
                )
        else:
            print(
                f"pseudo '{pseudo_proposer}' invalide ou non fourni ! vous aurez donc un pseudo generique"
            )

        pseudo_generique = f"Joueur{self.__id}"
        while pseudo_generique in Joueur.Joueurs_pseudos_uniques:
            self.__id += 1
            pseudo_generique = f"Joueur{self.__id}"

        Joueur.Joueurs_pseudos_uniques.add(pseudo_generique)
        print(f"Pseudo attribué : '{pseudo_generique}'")
        return pseudo_generique

    @property
    def pseudo(self):
        """getter pour le pseudo du joueur"""
        return self.__pseudo

    def ajouter_victoire(self):
        """Methode pour ajouter une victoire au joueur"""
        score = 1
        if self.__victoires_consecutives >= 3:
            score += 1  # +1 bonus si série de victoires consécutives
        self.__scores.append(score)
        self.__victoires_consecutives += 1

    @log_result
    def quitter(self):  # inutilisé mais peut servire
        """Methode pour nettoyer un attribut de la class avant de quitter le jeu pour un client qui quitte si on avait la possibiliter de revenire peut servire"""
        self.__victoires_consecutives = 0

    def get_scores(self):  # inutilisé mais peut servire
        return sorted(self.__scores, reverse=True)

    def scores_detail(self):  # inutilisé mais peut servire
        """Methode pour obtenir les scores des instances de joueur"""
        for score in self.__scores:
            yield score

    def calculer_score_total(self):
        """Methode pour calculer le score total du joueur"""
        return sum(map(lambda x: x, self.__scores))

    def __str__(self):
        """Methode speciale pour afficher le joueur"""
        return f"Joueur {self.__id}: {self.__pseudo}, Score total: {self.calculer_score_total()}, {self.pion}"

    def __eq__(self, other):
        return isinstance(other, Joueur) and self.__pseudo == other.pseudo

    def __lt__(self, other):
        return self.calculer_score_total() < other.calculer_score_total()

    @staticmethod
    def meilleurs_scores(joueurs):
        """Methode pour obtenir les meilleurs scores parmit les instances des joueurs"""
        return sorted(
            joueurs, key=lambda joueur: joueur.calculer_score_total(), reverse=True
        )
