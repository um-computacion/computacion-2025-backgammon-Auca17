import unittest
from core.board import Board  # Assuming board.py contains a Board class


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        # Test that the board initializes with correct starting positions
        self.assertEqual(
            len(self.board.__points_status__), 24
        )  # Assuming 24 points in backgammon
        # Add assertions for initial checker placements, e.g., point 0 has 2 checkers, etc.

    def test_move_checker(self):
        """
        Verifica que mover una ficha actualiza correctamente el conteo de fichas en los puntos.
        """
        initial_count = self.board.__points_status__[0]["count"]
        # El color correcto para el punto 0 inicial es 'white'
        self.board.move_checker(
            "white", 0, 1
        )  # Mueve una ficha blanca del punto 0 al 1
        self.assertEqual(self.board.__points_status__[0]["count"], initial_count - 1)
        self.assertEqual(self.board.__points_status__[1]["count"], 1)


if __name__ == "__main__":
    unittest.main()
