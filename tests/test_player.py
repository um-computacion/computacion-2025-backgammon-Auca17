"""
Este módulo contiene las pruebas unitarias para la clase Player.
"""

import unittest
from core.player import Player
from core.checker import Checker


class TestPlayer(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Player.
    """

    def setUp(self):
        """
        Configura una instancia de Player antes de cada prueba.
        """
        self.player = Player("Alice", "white")

    def test_initialization(self):
        """
        Verifica que el jugador se inicializa correctamente.
        """
        self.assertEqual(self.player.get_name(), "Alice")
        self.assertEqual(self.player.__color__, "white")
        self.assertEqual(self.player.get_bar_checkers(), 0)
        self.assertEqual(self.player.get_home_checkers(), 0)

    def test_add_and_get_bar_checkers(self):
        """
        Verifica que el contador de fichas en la barra se incrementa correctamente.
        """
        self.player.add_bar_checker()
        self.player.add_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), 2)

    def test_remove_bar_checker(self):
        """
        Verifica que el contador de fichas en la barra se decrementa correctamente.
        """
        self.player.add_bar_checker()
        self.player.add_bar_checker()
        self.player.remove_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), 1)
        self.player.remove_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), 0)

    def test_remove_bar_checker_from_empty_bar(self):
        """
        Verifica que intentar decrementar una barra vacía no causa errores.
        """
        self.player.remove_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), 0)

    def test_add_and_get_home_checkers(self):
        """
        Verifica que el contador de fichas en casa se incrementa correctamente.
        """
        self.player.add_home_checker()
        self.player.add_home_checker()
        self.assertEqual(self.player.get_home_checkers(), 2)

    def test_add_checker(self):
        """
        Verifica que se puede agregar una ficha a la lista de fichas del jugador.
        """
        checker = Checker("white")
        self.player.add_checker(checker)
        self.assertIn(checker, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 1)

    def test_remove_existing_checker(self):
        """
        Verifica que una ficha existente se puede eliminar de la lista.
        """
        checker = Checker("white")
        self.player.add_checker(checker)
        self.player.remove_checker(checker)
        self.assertNotIn(checker, self.player.checkers)

    def test_remove_non_existing_checker(self):
        """
        Verifica que intentar eliminar una ficha no existente no causa errores.
        """
        checker1 = Checker("white")
        checker2 = Checker("white")
        self.player.add_checker(checker1)
        self.player.remove_checker(checker2)
        self.assertIn(checker1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 1)

    def test_add_bar_checker_no_checker_object(self):
        """
        Verifica que el contador de fichas en la barra se incrementa
        cuando se llama a add_bar_checker sin un objeto checker.
        """
        initial_bar_checkers = self.player.get_bar_checkers()
        self.player.add_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), initial_bar_checkers + 1)


if __name__ == "__main__":
    unittest.main()
