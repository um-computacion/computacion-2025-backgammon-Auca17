"""
Este módulo contiene las pruebas unitarias para la clase Board.
"""

import unittest
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Board.

    Valida el correcto funcionamiento del tablero de Backgammon, incluyendo
    la inicialización, movimientos de fichas, capturas, bear-off y reingreso
    desde la barra.

    Methods
    -------
    setUp()
        Configura una instancia limpia del tablero antes de cada prueba
    test_initialization()
        Verifica la correcta inicialización del tablero con 24 puntos
    test_move_checker()
        Verifica que mover fichas actualiza correctamente los conteos
    test_get_2d_representation()
        Verifica la generación de la representación visual del tablero
    test_move_checker_from_empty_point()
        Verifica que no se puede mover desde un punto vacío
    test_move_checker_wrong_color()
        Verifica que no se puede mover fichas del color incorrecto
    test_move_checker_to_blocked_point()
        Verifica que no se puede mover a puntos bloqueados por el oponente
    test_move_checker_out_of_bounds()
        Verifica que no se permite mover fuera de los límites del tablero
    test_move_checker_and_capture()
        Verifica el mecanismo de captura de fichas del oponente
    test_bear_off_checker_valid()
        Verifica que las fichas pueden ser retiradas correctamente
    test_bear_off_checker_invalid()
        Verifica que no se puede hacer bear-off desde puntos vacíos
    test_enter_from_captured()
        Verifica el reingreso de fichas capturadas al tablero
    test_enter_from_captured_to_blocked_point()
        Verifica que no se puede reingresar a puntos bloqueados
    test_enter_from_captured_with_empty_bar()
        Verifica que no se puede reingresar si no hay fichas en la barra
    test_get_point()
        Verifica la obtención correcta de fichas de un punto específico
    test_get_2d_representation_with_captured_checkers()
        Verifica la representación visual con fichas capturadas
    """

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

    def test_get_point(self):
        """
        Verifica que get_point devuelve la lista correcta de fichas para un punto.
        Precondición: El tablero está en su estado inicial.
        Resultado: El punto 0 debe contener 2 fichas blancas.
        """
        point_content = self.board.get_point(0)
        self.assertEqual(len(point_content), 2)
        self.assertEqual(point_content[0].__color__, "white")

    def test_get_2d_representation_with_captured_checkers(self):
        """
        Verifica que la representación 2D muestra correctamente las fichas capturadas.
        Precondición: Se captura una ficha de cada color.
        Resultado: La representación de la barra debe mostrar 'W:1 B:1'.
        """
        # Capturamos una ficha blanca
        self.board.get_point(0).pop()
        self.board.move_checker("black", 12, 0)
        # Capturamos una ficha negra
        self.board.get_point(23).pop()
        self.board.move_checker("white", 11, 23)

        representation = self.board.get_2d_representation()
        self.assertIn("B:1 N:1", representation)

    def test_bear_off_checker_wrong_color(self):
        """
        Verifica que se lanza un ValueError al intentar hacer bear off de una ficha
        desde un punto que contiene fichas del color opuesto.
        """
        # El punto 0 contiene fichas blancas. Intentamos hacer bear off de una negra.
        with self.assertRaises(ValueError):
            self.board.bear_off("black", 0)

    def test_get_home(self):
        """
        Verifica que get_home devuelve la lista correcta de fichas que han salido.
        """
        # Preparamos el escenario: vaciamos el punto 23 y movemos una ficha blanca allí.
        self.board.get_point(23).pop()
        self.board.get_point(23).pop()
        self.board.move_checker("white", 18, 23)

        self.board.bear_off("white", 23)
        home_checkers = self.board.get_home("white")
        self.assertEqual(len(home_checkers), 1)
        self.assertEqual(home_checkers[0].__color__, "white")

    def test_enter_from_captured_and_capture(self):
        """
        Verifica que reingresar una ficha a un punto con una sola ficha oponente la captura.
        """
        # Preparamos el escenario: una ficha negra solitaria en el punto 2.
        self.board.move_checker("black", 23, 2)
        # Capturamos una ficha blanca para tenerla en la barra.
        self.board.get_point(0).pop()  # Vaciamos el punto
        self.board.move_checker("black", 12, 0)

        # Ahora, la ficha blanca reingresa al punto 2, capturando a la negra.
        self.board.enter_from_captured("white", 2)

        self.assertEqual(len(self.board.get_captured("white")), 0)
        self.assertEqual(len(self.board.get_captured("black")), 1)
        self.assertEqual(self.board.get_point_count(2), 1)
        self.assertEqual(self.board.get_point(2)[0].__color__, "white")

    def test_get_2d_representation_with_stack_counter(self):
        """
        Verifica que la representación 2D muestra un contador para más de 5 fichas.
        """
        # Añadimos fichas al punto 0 para que tenga 6 fichas blancas.
        for _ in range(4):
            self.board.get_point(0).append(Checker("white"))

        representation = self.board.get_2d_representation()
        self.assertIn("x6", representation)


if __name__ == "__main__":
    unittest.main()
