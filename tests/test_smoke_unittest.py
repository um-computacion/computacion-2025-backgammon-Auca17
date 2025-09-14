import unittest
from core.board import Board
from core.checker import Checker

class SmokeTests(unittest.TestCase):
    def test_board_has_dunder_points(self):
        b = Board()
        # dunder SIN name-mangling
        self.assertTrue(hasattr(b, "__points__"))

    def test_checker_moves_and_capture(self):
        c = Checker("WHITE", 0)
        c.move_to(5)
        self.assertEqual(getattr(c, "__position__"), 5)
        c.capture()
        self.assertTrue(getattr(c, "__is_captured__"))
        self.assertEqual(getattr(c, "__position__"), "bar")

