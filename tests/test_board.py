import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        """
        Verifica que el tablero se inicializa con las posiciones de inicio correctas.
        """
        self.assertEqual(len(self.board.__points_status__), 24)

    def test_move_checker(self):
        """
        Verifica que mover una ficha actualiza correctamente el conteo de fichas en los puntos.
        """
        __initial_count__ = self.board.__points_status__[0]["count"]
        # El color correcto para el punto 0 inicial es 'white'
        self.board.move_checker("white", 0, 1)
        self.assertEqual(
            self.board.__points_status__[0]["count"], __initial_count__ - 1
        )
        self.assertEqual(self.board.__points_status__[1]["count"], 1)

    def test_get_2d_representation(self):
        """
        Verifica que la representación 2D del tablero se genera correctamente.
        """
        __representation__ = self.board.get_2d_representation()
        self.assertIsInstance(__representation__, str)
        self.assertIn("| BAR |", __representation__)
        self.assertIn("12 11 10  9  8  7", __representation__)
        self.assertIn("13 14 15 16 17 18", __representation__)

    def test_move_checker_from_empty_point(self):
        """
        Verifica que se lanza un ValueError al intentar mover desde un punto vacío.
        """
        with self.assertRaises(ValueError):
            self.board.move_checker("white", 2, 3)

    def test_move_checker_wrong_color(self):
        """
        Verifica que se lanza un ValueError al intentar mover una ficha del color incorrecto.
        """
        with self.assertRaises(ValueError):
            self.board.move_checker("black", 0, 1)

    def test_move_checker_to_blocked_point(self):
        """
        Verifica que se lanza un ValueError al intentar mover a un punto bloqueado por el oponente.
        """
        # El punto 5 está bloqueado por 5 fichas negras.
        with self.assertRaises(ValueError):
            self.board.move_checker("white", 0, 5)

    def test_move_checker_out_of_bounds(self):
        """
        Verifica que se lanza un IndexError al mover fuera de los límites del tablero.
        """
        with self.assertRaises(IndexError):
            self.board.move_checker("white", 0, 24)
        with self.assertRaises(IndexError):
            self.board.move_checker("white", -1, 1)

    def test_move_checker_and_capture(self):
        """
        Verifica que mover una ficha a un punto con una sola ficha oponente la captura.
        """
        # Preparamos el escenario: movemos una ficha negra a un punto vacío.
        self.board.move_checker("black", 23, 2)
        # Ahora movemos una ficha blanca a ese mismo punto para capturar la negra.
        self.board.move_checker("white", 0, 2)

        self.assertEqual(len(self.board.get_captured("black")), 1)
        self.assertEqual(self.board.get_point_count(2), 1)
        self.assertEqual(self.board.get_point(2)[0].__color__, "white")

    def test_bear_off_checker_valid(self):
        """
        Verifica que una ficha puede ser retirada del tablero (bear off) correctamente.
        """
        # Preparamos el escenario: vaciamos el punto 23 y movemos una ficha blanca allí.
        self.board.get_point(23).pop()
        self.board.get_point(23).pop()
        self.board.move_checker("white", 18, 23)
        self.board.bear_off("white", 23)
        self.assertEqual(len(self.board.get_home("white")), 1)
        self.assertEqual(self.board.get_point_count(23), 0)

    def test_bear_off_checker_invalid(self):
        """
        Verifica que se lanza un ValueError al intentar hacer bear off desde un punto vacío.
        """
        with self.assertRaises(ValueError):
            self.board.bear_off("white", 2)

    def test_enter_from_captured(self):
        """
        Verifica que una ficha capturada puede reingresar al tablero.
        """
        # Preparamos el escenario: dejamos una sola ficha blanca en el punto 0 para ser capturada.
        self.board.get_point(0).pop()
        self.board.move_checker("black", 12, 0)
        self.assertEqual(len(self.board.get_captured("white")), 1)

        # Ahora, la reingresamos en un punto válido (ej. punto 21, que está vacío)
        self.board.enter_from_captured("white", 21)
        self.assertEqual(len(self.board.get_captured("white")), 0)
        self.assertEqual(self.board.get_point_count(21), 1)
        self.assertEqual(self.board.get_point(21)[0].__color__, "white")

    def test_enter_from_captured_to_blocked_point(self):
        """
        Verifica que no se puede reingresar una ficha a un punto bloqueado.
        """
        # Preparamos el escenario: capturamos una ficha blanca.
        self.board.get_point(0).pop()
        self.board.move_checker("black", 12, 0)
        # El punto 5 está bloqueado por fichas negras.
        with self.assertRaises(ValueError):
            self.board.enter_from_captured("white", 5)

    def test_enter_from_captured_with_empty_bar(self):
        """
        Verifica que se lanza un ValueError si no hay fichas en la barra para reingresar.
        """
        with self.assertRaises(ValueError):
            self.board.enter_from_captured("white", 20)


if __name__ == "__main__":
    unittest.main()
