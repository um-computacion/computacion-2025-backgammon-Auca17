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

    def test_initialization(self):
        """
        Verifica que el jugador se inicializa correctamente.
        Precondición: Se crea un Player con nombre y color.
        Resultado: Los atributos se asignan correctamente.
        """
        player = Player("Alice", "white")
        self.assertEqual(player.get_name(), "Alice")
        self.assertEqual(player.__color__, "white")
        self.assertEqual(player.get_bar_checkers(), 0)
        self.assertEqual(player.get_home_checkers(), 0)

    def test_add_and_get_bar_checkers(self):
        """
        Verifica que el contador de fichas en la barra se incrementa correctamente.
        Precondición: Jugador sin fichas en la barra.
        Resultado: El contador se incrementa a 2.
        """
        player = Player("Alice", "white")
        player.add_bar_checker()
        player.add_bar_checker()
        self.assertEqual(player.get_bar_checkers(), 2)

    def test_remove_bar_checker(self):
        """
        Verifica que el contador de fichas en la barra se decrementa correctamente.
        Precondición: Jugador con 2 fichas en la barra.
        Resultado: El contador disminuye a 1 y luego a 0.
        """
        player = Player("Alice", "white")
        player.add_bar_checker()
        player.add_bar_checker()
        player.remove_bar_checker()
        self.assertEqual(player.get_bar_checkers(), 1)
        player.remove_bar_checker()
        self.assertEqual(player.get_bar_checkers(), 0)

    def test_remove_bar_checker_from_empty_bar(self):
        """
        Verifica que intentar decrementar una barra vacía no causa errores.
        Precondición: Jugador sin fichas en la barra.
        Resultado: El contador permanece en 0.
        """
        player = Player("Alice", "white")
        player.remove_bar_checker()
        self.assertEqual(player.get_bar_checkers(), 0)

    def test_add_and_get_home_checkers(self):
        """
        Verifica que el contador de fichas en casa se incrementa correctamente.
        Precondición: Jugador sin fichas en casa.
        Resultado: El contador se incrementa a 2.
        """
        player = Player("Alice", "white")
        player.add_home_checker()
        player.add_home_checker()
        self.assertEqual(player.get_home_checkers(), 2)

    def test_add_checker(self):
        """
        Verifica que se puede agregar una ficha a la lista de fichas del jugador.
        Precondición: El jugador tiene una lista de fichas vacía.
        Resultado: La ficha se añade y la lista contiene 1 elemento.
        """
        player = Player("Carol", "black")
        checker = Checker("black")
        player.add_checker(checker)
        self.assertIn(checker, player.checkers)
        self.assertEqual(len(player.checkers), 1)

    def test_remove_existing_checker(self):
        """
        Verifica que una ficha existente se puede eliminar de la lista.
        Precondición: El jugador tiene una ficha en su lista.
        Resultado: La ficha se elimina y la lista queda vacía.
        """
        player = Player("Carol", "black")
        checker = Checker("black")
        player.add_checker(checker)
        player.remove_checker(checker)
        self.assertNotIn(checker, player.checkers)

    def test_remove_non_existing_checker(self):
        """
        Verifica que intentar eliminar una ficha no existente no causa errores.
        Precondición: El jugador tiene una ficha y se intenta eliminar otra.
        Resultado: La lista de fichas no cambia.
        """
        player = Player("Carol", "black")
        checker1 = Checker("black")
        checker2 = Checker("black")
        player.add_checker(checker1)
        player.remove_checker(checker2)
        self.assertIn(checker1, player.checkers)
        self.assertEqual(len(player.checkers), 1)


if __name__ == "__main__":
    unittest.main()
