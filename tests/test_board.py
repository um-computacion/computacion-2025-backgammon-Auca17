import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        """
        Verifica que el tablero se inicializa con las posiciones de inicio correctas.
        """
        self.assertEqual(
            len(self.board.__points_status__), 24
        )

    def test_move_checker(self):
        """
        Verifica que mover una ficha actualiza correctamente el conteo de fichas en los puntos.
        """
        __initial_count__ = self.board.__points_status__[0]["count"]
        # El color correcto para el punto 0 inicial es 'white'
        self.board.move_checker(
            "white", 0, 1
        )
        self.assertEqual(self.board.__points_status__[0]["count"], __initial_count__ - 1)
        self.assertEqual(self.board.__points_status__[1]["count"], 1)


if __name__ == "__main__":
    unittest.main()
