import unittest
from core.game import Game
from core.player import Player
from core.board import Board

class TestGame(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Game.
    Cada método de prueba verifica un aspecto específico del comportamiento del juego.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        Crea dos jugadores y un juego para usar en las pruebas.
        """
        self.player1 = Player("Alice", "white", [])
        self.player2 = Player("Bob", "black", [])
        self.game = Game(self.player1, self.player2)

    def test_initialization(self):
        """
        Verifica que el juego se inicialice correctamente con dos jugadores,
        un tablero vacío, turno inicial en 0 y sin ganador.
        """
        self.assertIsInstance(self.game.__board__, Board)
        self.assertEqual(len(self.game.__players__), 2)
        self.assertEqual(self.game.__current_turn__, 0)
        self.assertIsNone(self.game.__winner__)

    def test_switch_turn(self):
        """
        Verifica que el turno cambie correctamente entre los dos jugadores.
        """
        self.assertEqual(self.game.__current_turn__, 0)
        self.game.switch_turn()
        self.assertEqual(self.game.__current_turn__, 1)
        self.game.switch_turn()
        self.assertEqual(self.game.__current_turn__, 0)


if __name__ == '__main__':
    unittest.main()
