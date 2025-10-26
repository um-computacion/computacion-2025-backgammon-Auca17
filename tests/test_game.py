import unittest
from unittest.mock import patch
from core.game import Game
from core.player import Player
from core.board import Board
from core.checker import Checker
from core.dice import Dice


class TestGame(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Game.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        """
        self.__player1__ = Player("Alice", "white")
        self.__player2__ = Player("Bob", "black")
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__game__ = Game(
            player1=self.__player1__,
            player2=self.__player2__,
            board=self.__board__,
            dice=self.__dice__,
        )

    def test_initialization(self):
        """
        Verifica que el juego se inicializa correctamente.
        """
        self.assertIsInstance(self.__game__.__board__, Board)
        self.assertEqual(len(self.__game__.__players__), 2)
        self.assertEqual(self.__game__.__current_turn__, 0)
        self.assertIsNone(self.__game__.__winner__)

    def test_switch_turn(self):
        """
        Verifica que el turno cambia correctamente entre jugadores.
        """
        __initial_turn__ = self.__game__.__current_turn__
        self.__game__.switch_turn()
        self.assertNotEqual(self.__game__.__current_turn__, __initial_turn__)
        self.__game__.switch_turn()
        self.assertEqual(self.__game__.__current_turn__, __initial_turn__)

    @patch("core.dice.Dice.roll")
    def test_start_rolls_dice(self, __mock_roll__):
        """
        Verifica que el método start realiza la primera tirada de dados.
        """
        # Simulamos que los dados sacan (5, 2) y que no es un doble
        self.__game__.__dice__.get_values = lambda: (5, 2)
        self.__game__.__dice__.is_double = lambda: False

        # Llamamos a start
        self.__game__.start()

        # Verificamos que los valores de los dados se han establecido
        self.assertEqual(self.__game__.__dice_values__, [5, 2])

    def test_make_move_valid(self):
        """
        Verifica que un movimiento válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        __from_pos__ = 0 if __player__.__color__ == "white" else 23
        __to_pos__ = __from_pos__ + (3 if __player__.__color__ == "white" else -3)
        self.assertTrue(self.__game__.make_move(__from_pos__, __to_pos__))
        self.assertNotIn(3, self.__game__.__dice_values__)

    def test_make_move_invalid(self):
        """
        Verifica que un movimiento inválido lanza un ValueError.
        """
        self.__game__.start()
        self.__game__.__dice_values__ = [3, 4]
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 1)

    def test_reentry_valid(self):
        """
        Verifica que un movimiento de reingreso válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        self.__game__.__board__.get_captured(__player__.__color__).append(
            Checker(__player__.__color__)
        )
        __to_pos__ = 2 if __player__.__color__ == "white" else 20
        self.assertTrue(self.__game__.make_move(0, __to_pos__))

    def test_reentry_white_bug_fix(self):
        """
        Verifica que un jugador blanco puede reingresar desde la barra.
        """
        self.__game__.start()
        __player__ = self.__player1__
        self.__game__.__current_turn__ = 0
        self.__game__.__dice_values__ = [3, 4]
        self.__game__.__board__.get_captured(__player__.__color__).append(
            Checker(__player__.__color__)
        )
        self.assertTrue(self.__game__.make_move(0, 2))

    def test_bear_off_valid(self):
        """
        Verifica que un movimiento de sacar ficha válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        # Prepara el tablero para sacar fichas
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        if __player__.__color__ == "white":
            self.__game__.__board__.__points__[20] = [Checker(__player__.__color__)] * 2
            self.assertTrue(self.__game__.make_move(20, 24))
        else:
            self.__game__.__board__.__points__[3] = [Checker(__player__.__color__)] * 2
            self.assertTrue(self.__game__.make_move(3, -1))

    def test_win_condition(self):
        """
        Verifica que la condición de victoria se detecta correctamente.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        for i in range(15):
            self.__game__.__board__.get_home(__player__.__color__).append(
                Checker(__player__.__color__)
            )
        self.__game__.check_winner()
        self.assertEqual(self.__game__.get_winner(), __player__)

    def test_get_possible_moves_no_moves(self):
        """
        Verifica que se devuelve una lista vacía cuando no hay movimientos posibles.
        """
        # Forzar el turno del jugador blanco para hacer el test determinista
        self.__game__.__current_turn__ = 0
        self.__player__ = self.__game__.get_current_player()
        # Bloquear todos los movimientos posibles
        for i in range(6):
            color_oponente = (
                "black" if self.__player__.__color__ == "white" else "white"
            )
            # Asumiendo que el jugador blanco está en el punto 0
            # Bloquear los 6 puntos siguientes
            if self.__player__.__color__ == "white":
                self.__game__.__board__.__points__[i + 1] = [
                    Checker(color_oponente)
                ] * 2
        self.__game__.__dice_values__ = [1, 2, 3, 4, 5, 6]

        # Vaciar otros puntos para asegurar que solo el punto 0 tenga fichas
        for i in range(1, 24):
            if i > 6 or i == 0:
                self.__game__.__board__.__points__[i] = []

        # Colocar una ficha blanca en el punto 0
        if self.__player__.__color__ == "white":
            self.__game__.__board__.__points__[0] = [Checker("white")]

        __possible_moves__ = self.__game__.get_possible_moves()
        self.assertEqual(len(__possible_moves__), 0)


if __name__ == "__main__":
    unittest.main()
