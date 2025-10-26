import unittest
from core.game import Game
from core.player import Player
from core.board import Board
from core.dice import Dice


class TestBackgammonExceptions(unittest.TestCase):
    def setUp(self):
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
        self.__game__.start()

    def test_invalid_move_exception(self):
        """
        Verifica que un movimiento inválido lanza un ValueError.
        """
        self.__game__.__dice_values__ = [1, 2]
        # Intenta mover desde un punto vacío
        with self.assertRaises(ValueError):
            self.__game__.make_move(2, 3)

    def test_out_of_bounds_exception(self):
        """
        Verifica que un movimiento fuera de los límites del tablero lanza un IndexError.
        """
        self.__game__.__dice_values__ = [1, 2]
        with self.assertRaises(IndexError):
            self.__game__.make_move(25, 1)

    def test_insufficient_dice_exception(self):
        """
        Verifica que un movimiento que no coincide con el dado lanza un ValueError.
        """
        self.__game__.__dice_values__ = [1, 2]
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 5)


if __name__ == "__main__":
    unittest.main()
