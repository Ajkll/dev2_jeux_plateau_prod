from .plateau import Plateau


class ChangementMap:
    def __init__(self, taille_nouvelle_map):
        self.taille_nouvelle_map = taille_nouvelle_map

    def appliquer_changement(self, jeu):
        nouvelle_map = Plateau(self.taille_nouvelle_map)
        jeu.plateau = nouvelle_map

        for pion in jeu.pions:
            pion.position = 0
