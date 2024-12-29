class Pion:
    def __init__(self, nom):
        self.nom = nom
        self.position = 0

    def deplacer(self, pas):
        self.position = max(0, self.position + pas)  

    def reset(self):
        self.position = 0

    def __str__(self):
        return f"{self.nom}, vous êtes à la position {self.position}."
