import random


class Plateau:
    def __init__(self, taille=10, cases_speciales=None):

        self.taille = taille
        self.cases = [f"Case {i}" for i in range(taille)]
        self.cases_speciales = cases_speciales if cases_speciales else {}

    def obtenir_effet_case(self, case):

        return self.cases_speciales.get(case, None)

    def afficher_cases(self):

        return self.cases

    @staticmethod
    def generer_cases_speciales(taille, effets_possibles):
        nombre_cases = random.randint(3, 7)
        cases_speciales = {}
        while len(cases_speciales) < nombre_cases:
            case = random.randint(1, taille - 2)
            if case not in cases_speciales:
                effet = random.choice(effets_possibles)
                cases_speciales[case] = effet
        return cases_speciales

    def cases_avec_effet(self, effet_recherche):
        cases_trouvees = []
        for case, effet in self.cases_speciales.items():
            if effet == effet_recherche:
                cases_trouvees.append(case)
        return cases_trouvees

    def __str__(self):
        description = []
        for i in range(self.taille):
            case_info = f"Case {i}"
            if i in self.cases_speciales:
                case_info += f" ({self.cases_speciales[i]})"
            description.append(case_info)
        return f"Plateau: {', '.join(description)}"
