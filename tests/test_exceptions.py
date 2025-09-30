# c:\Users\Rufda\Desktop\Python\computacion-2025-backgammon-Auca17\test_exceptions.py
import unittest
from core.game import Game as BackgammonGame  # Relative import from parent directory

class TestBackgammonExceptions(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()

    def test_invalid_move_exception(self):
        # Test for invalid move, e.g., moving a piece to an occupied point
        with self.assertRaises(ValueError):
            self.game.make_move(1, 2)  # Example invalid move

    def test_out_of_bounds_exception(self):
        # Test for move beyond board limits
        with self.assertRaises(IndexError):
            self.game.make_move(25, 1)  # Point 25 doesn't exist

    def test_insufficient_dice_exception(self):
        # Test for move not matching dice roll
        with self.assertRaises(ValueError):
            self.game.make_move(1, 6)  # If dice rolled 1 and 2, say

if __name__ == '__main__':
    unittest.main()