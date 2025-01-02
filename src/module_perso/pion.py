class Pion:
    def __init__(self, nom):
        self.nom = nom
        self.position = 0

    def deplacer(self, deplacement):
        if deplacement < 0:
            raise ValueError("Le nombre de pas doit être positif.")
        self.position += deplacement

    def reculer(self, deplacement):
        self.position = max(0, self.position - deplacement)

    def sur_case(self, case):
        return self.position == case

    def __str__(self):
        return f"{self.nom}, vous êtes à la position {self.position}."
