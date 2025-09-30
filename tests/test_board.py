import unittest
from core.board import Board  # Assuming board.py contains a Board class

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        # Test that the board initializes with correct starting positions
        self.assertEqual(len(self.board.points), 24)  # Assuming 24 points in backgammon
        # Add assertions for initial checker placements, e.g., point 0 has 2 checkers, etc.

    def test_move_checker(self):
        # Test moving a checker from one point to another
        initial_count = self.board.points[0]['count']
        self.board.move_checker(0, 1, 1)  # Move 1 checker from point 0 to point 1
        self.assertEqual(self.board.points[0]['count'], initial_count - 1)
        self.assertEqual(self.board.points[1]['count'], initial_count + 1)

    def test_invalid_move(self):
        # Test that invalid moves raise an exception
        with self.assertRaises(ValueError):
            self.board.move_checker(0, 1, 10)  # Trying to move more checkers than available

    def test_bearing_off(self):
        # Test bearing off checkers when in home board
        # Set up a scenario where bearing off is possible
        self.board.points[23]['count'] = 1  # Assuming point 23 is home
        self.board.bear_off(23)
        self.assertEqual(self.board.points[23]['count'], 0)
        # Assert that the checker is added to the borne off count

    # Add more tests as needed based on board.py methods

if __name__ == '__main__':
    unittest.main()
