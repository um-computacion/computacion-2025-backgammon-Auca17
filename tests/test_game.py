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
        self.assertIsInstance(self.game._Game__board__, Board)
        self.assertEqual(len(self.game._Game__players__), 2)
        self.assertEqual(self.game._Game__current_turn__, 0)
        self.assertIsNone(self.game._Game__winner__)

    def test_switch_turn(self):
        """
        Verifica que el turno cambie correctamente entre los dos jugadores.
        """
        self.assertEqual(self.game._Game__current_turn__, 0)
        self.game.switch_turn()
        self.assertEqual(self.game._Game__current_turn__, 1)
        self.game.switch_turn()
        self.assertEqual(self.game._Game__current_turn__, 0)

    def test_get_current_player(self):
        """
        Verifica que se devuelva el jugador correcto según el turno actual.
        """
        self.assertEqual(self.game.get_current_player(), self.player1)
        self.game.switch_turn()
        self.assertEqual(self.game.get_current_player(), self.player2)

    def test_is_over_and_get_winner(self):
        """
        Verifica que el juego no esté terminado inicialmente y que no haya ganador.
        """
        self.assertFalse(self.game.is_over())
        self.assertIsNone(self.game.get_winner())

    def test_make_move_valid(self):
        """
        Verifica que un movimiento válido se ejecute correctamente.
        Asume una configuración simplificada donde el tablero permite movimientos adyacentes.
        """
        # Configurar tablero para un movimiento válido (simplificado)
        self.game._Game__board__._Board__points = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = self.game.make_move(self.player1, 0, 1)
        self.assertTrue(result)
        self.assertEqual(self.game._Game__board__._Board__points[0], 0)
        self.assertEqual(self.game._Game__board__._Board__points[1], 1)

    def test_make_move_invalid_out_of_bounds(self):
        """
        Verifica que un movimiento fuera de los límites del tablero sea rechazado.
        """
        result = self.game.make_move(self.player1, -1, 0)
        self.assertFalse(result)
        result = self.game.make_move(self.player1, 0, 24)
        self.assertFalse(result)

    def test_make_move_invalid_no_checker(self):
        """
        Verifica que un movimiento sea rechazado si no hay ficha del jugador en la posición de origen.
        """
        result = self.game.make_move(self.player1, 0, 1)
        self.assertFalse(result)

    def test_make_move_invalid_landing_on_opponent(self):
        """
        Verifica que un movimiento sea rechazado si intenta aterrizar en una posición ocupada por el oponente.
        """
        # Configurar tablero con oponente en posición 1
        self.game._Game__board__._Board__points = [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = self.game.make_move(self.player1, 0, 1)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
