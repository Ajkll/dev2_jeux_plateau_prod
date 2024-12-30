class Pion:
    def __init__(self, nom):
        self.nom = nom
        self.position = 0

    def deplacer(self, pas):
        """bouge le pion de 'pas' case"""
        self.position = max(0, self.position + pas)

    def reset(self):
        """remet le pion sur la case 0"""
        self.position = 0

    def __str__(self):
        return f"{self.nom}, vous êtes à la position {self.position}."
