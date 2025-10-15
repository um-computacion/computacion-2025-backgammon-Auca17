import unittest
from core.player import Player


class TestPlayer(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Player.
    Cada método de prueba verifica un aspecto específico del comportamiento del jugador.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        Crea un jugador para usar en las pruebas.
        """
        self.player = Player("Alice", "white", [])

    def test_initialization(self):
        """
        Verifica que el jugador se inicialice correctamente con nombre, color y lista de fichas vacía.
        """
        self.assertEqual(self.player.__name__, "Alice")
        self.assertEqual(self.player.__color__, "white")
        self.assertEqual(self.player.__checkers__, [])

    def test_add_checker(self):
        """
        Verifica que se pueda agregar una ficha a la lista de fichas del jugador.
        """
        self.player.add_bar_checker(1)
        self.assertIn(1, self.player.__checkers__)
        self.assertEqual(len(self.player.__checkers__), 1)

    def test_remove_checker(self):
        """
        Verifica que se pueda remover una ficha existente de la lista de fichas del jugador.
        """
        self.player.add_checker(1)
        self.player.remove_checker(1)
        self.assertNotIn(1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 0)


if __name__ == "__main__":
    unittest.main()
