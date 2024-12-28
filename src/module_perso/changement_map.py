from .plateau import Plateau


class Changement_map:
    def __init__(self, taille_nouvelle_map, cases_speciales=None):
        self.taille_nouvelle_map = taille_nouvelle_map
        self.cases_speciales = cases_speciales or {}

    def appliquer_changement(self, jeu):
        nouvelle_map = Plateau(self.taille_nouvelle_map, self.cases_speciales)
        jeu.plateau = nouvelle_map

        for pion in jeu.pions:
            pion.position = 0
