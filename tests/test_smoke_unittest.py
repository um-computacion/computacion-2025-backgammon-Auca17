import unittest
from core.board import Board

class SmokeTests(unittest.TestCase):
    def test_board_exists(self):
        self.assertTrue(hasattr(Board(), "_Board__points__"))

if __name__ == "__main__":
    unittest.main()
