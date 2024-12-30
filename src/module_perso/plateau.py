import random
from module_perso.logging_config import get_logger

logger = get_logger(__name__)


class ExceptionCustomGenerationCritiqueErreur(Exception):
    pass


class Plateau:
    def __init__(self, taille=10, cases_speciales=None):

        self._taille = taille
        self.cases_speciales = cases_speciales if cases_speciales else {}

    def obtenir_effet_case(self, case):
        """retourne l'effet de la case si elle existe, sinon None"""
        return self.cases_speciales.get(case, None)

    @property
    def taille(self):
        """getter qui retourne la taille du plateau"""
        return self._taille

    @staticmethod
    def generer_cases_speciales(taille, effets_possibles):
        """retourne un dictionnaire contenant les cases speciales et leur effets"""
        try:
            nombre_cases = random.randint(3, 7)
            cases_speciales = {}
            while len(cases_speciales) < nombre_cases:
                case = random.randint(1, taille - 2)
                if case not in cases_speciales:
                    effet = random.choice(effets_possibles)
                    cases_speciales[case] = effet
            return cases_speciales
        except ExceptionCustomGenerationCritiqueErreur:
            logger.exception(
                "Une erreur critique s'est produite lors de la generation des cases speciales"
            )
            exit(-1)  # si cela arrive le programme dois s'arreter

    def __str__(self):
        description = []
        for i in range(self.taille):
            case_info = f"Case {i}"
            if i in self.cases_speciales:
                case_info += f" ({self.cases_speciales[i]})"
            description.append(case_info)
        return f"Plateau: {', '.join(description)}"
