import unittest
from core.player import Player


class TestPlayer(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Player.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        """
        self.__player__ = Player("Alice", "white", [])

    def test_initialization(self):
        """
        Verifica que el jugador se inicializa correctamente.
        """
        self.assertEqual(self.__player__.__name__, "Alice")
        self.assertEqual(self.__player__.__color__, "white")
        self.assertEqual(self.__player__.__checkers__, [])

    def test_add_checker(self):
        """
        Verifica que se puede agregar una ficha a la lista de fichas del jugador.
        """
        self.__player__.add_bar_checker(1)
        self.assertIn(1, self.__player__.__checkers__)
        self.assertEqual(len(self.__player__.__checkers__), 1)

    def test_remove_checker(self):
        """
        Verifica que se puede eliminar una ficha de la lista de fichas del jugador.
        """
        self.__player__.add_checker(1)
        self.__player__.remove_checker(1)
        self.assertNotIn(1, self.__player__.checkers)
        self.assertEqual(len(self.__player__.checkers), 0)


if __name__ == "__main__":
    unittest.main()
