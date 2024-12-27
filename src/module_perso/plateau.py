class Plateau:
    def __init__(self, taille=10, cases_speciales=None):
        self.taille = taille
        self.cases = [f"Case {i}" for i in range(taille)]
        self.cases_speciales = cases_speciales

    def est_case_valide(self, case):
        return 0 <= case < self.taille

    def obtenir_effet_case(self, case):
        return self.cases_speciales.get(case, None)

    def afficher_cases(self):
        return self.cases

    def __str__(self):
        description = []
        for i in range(self.taille):
            case_info = f"Case {i}"
            if i in self.cases_speciales:
                case_info += f" ({self.cases_speciales[i]})"
            description.append(case_info)
        return "\n".join(description)
