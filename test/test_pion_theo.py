import unittest
from src.module_perso.pion import Pion


class TestPion(unittest.TestCase):
    def test_initialisation(self):
        pion = Pion("Pion 1")
        self.assertEqual(pion.nom, "Pion 1")
        self.assertEqual(pion.position, 0)

    def test_deplacer_avance(self):
        pion = Pion("Pion 1")
        pion.deplacer(5)
        self.assertEqual(pion.position, 5)
        pion.deplacer(3)
        self.assertEqual(pion.position, 8)

    def test_deplacer_recule(self):
        pion = Pion("Pion 1")
        pion.deplacer(5)
        pion.deplacer(-3)
        self.assertEqual(pion.position, 2)

    def test_deplacer_recule_sous_zero(self):
        pion = Pion("Pion 1")
        pion.deplacer(-3)
        self.assertEqual(pion.position, 0)

    def test_reset(self):
        pion = Pion("Pion 1")
        pion.deplacer(10)
        pion.reset()
        self.assertEqual(pion.position, 0)

    def test_str_representation(self):
        pion = Pion("Pion 1")
        self.assertEqual(str(pion), "Pion 1, vous êtes à la position 0.")
        pion.deplacer(5)
        self.assertEqual(str(pion), "Pion 1, vous êtes à la position 5.")


if __name__ == "__main__":
    unittest.main()
