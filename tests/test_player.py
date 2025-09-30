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
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(self.player.color, "white")
        self.assertEqual(self.player.checkers, [])

    def test_add_checker(self):
        """
        Verifica que se pueda agregar una ficha a la lista de fichas del jugador.
        """
        self.player.add_checker(1)
        self.assertIn(1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 1)

    def test_remove_checker(self):
        """
        Verifica que se pueda remover una ficha existente de la lista de fichas del jugador.
        """
        self.player.add_checker(1)
        self.player.remove_checker(1)
        self.assertNotIn(1, self.player.checkers)
        self.assertEqual(len(self.player.checkers), 0)

    def test_remove_checker_not_present(self):
        """
        Verifica que intentar remover una ficha no presente no cause errores y no modifique la lista.
        """
        initial_length = len(self.player.checkers)
        self.player.remove_checker(1)  # Ficha no presente
        self.assertEqual(len(self.player.checkers), initial_length)

    def test_get_checker_count(self):
        """
        Verifica que se devuelva correctamente el número de fichas del jugador.
        """
        self.assertEqual(self.player.get_checker_count(), 0)
        self.player.add_checker(1)
        self.player.add_checker(2)
        self.assertEqual(self.player.get_checker_count(), 2)


    def test_contador_fichas(self):
        """
        Verifica que add_home_checker incremente correctamente el contador de fichas en casa.
        """
        initial = self.player.get_home_checkers()
        self.player.add_home_checker()
        self.assertEqual(self.player.get_home_checkers(), initial + 1)

    def test_get_bar_checkers(self):
        """
        Verifica que get_bar_checkers devuelva el valor correcto del contador de fichas en la barra.
        """
        self.assertEqual(self.player.get_bar_checkers(), 0)
        self.player.add_bar_checker()
        self.assertEqual(self.player.get_bar_checkers(), 1)

    def test_get_home_checkers(self):
        """
        Verifica que get_home_checkers devuelva el valor correcto del contador de fichas en casa.
        """
        self.assertEqual(self.player.get_home_checkers(), 0)
        self.player.add_home_checker()
        self.assertEqual(self.player.get_home_checkers(), 1)

if __name__ == '__main__':
    unittest.main()
