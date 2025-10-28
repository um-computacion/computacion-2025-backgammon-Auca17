"""
Módulo de pruebas unitarias para la clase Board.

Este módulo contiene los tests que validan el funcionamiento del tablero
del juego, incluyendo la configuración inicial, colocación de fichas,
movimientos y gestión de la barra y bear-off.

Classes
-------
TestBoard
    Suite de pruebas para la clase Board
"""

import unittest
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Board.
    
    Valida que el tablero se inicialice correctamente con la configuración
    estándar de Backgammon y que todas las operaciones de manipulación
    de fichas funcionen como se espera.
    
    Attributes
    ----------
    board : Board
        Instancia del tablero utilizada en las pruebas
        
    Methods
    -------
    setUp()
        Configura el tablero antes de cada prueba
    test_init()
        Verifica la inicialización correcta del tablero
    test_place_checker()
        Verifica la colocación de fichas en el tablero
    test_remove_checker()
        Verifica la remoción de fichas del tablero
    test_move_checker()
        Verifica el movimiento de fichas entre posiciones
    test_get_bar()
        Verifica la obtención de fichas en la barra
    test_add_to_bar()
        Verifica añadir fichas a la barra
    test_remove_from_bar()
        Verifica remover fichas de la barra
    test_get_off()
        Verifica la obtención de fichas retiradas
    test_add_to_off()
        Verifica añadir fichas al bear-off
    test_display()
        Verifica que el método display no lance excepciones
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
        self.board.move_checker("white", 11, 2)
        self.assertEqual(self.board.__points_status__[2]["color"], "white")
        self.assertEqual(self.board.__points_status__[23]["count"], 0)

    def test_enter_from_captured(self):
        """
        Verifica que se puede reingresar una ficha desde la barra al tablero.
        Escenario: Una ficha blanca es capturada y se intenta reingresar.
        """
        # Capturamos una ficha blanca
        self.board.get_point(0).pop()
        self.board.move_checker("black", 12, 0)
        # Intentamos reingresar la ficha blanca desde la barra
        self.board.enter_from_captured("white", 5)
        self.assertEqual(self.board.__points_status__[5]["color"], "white")
        self.assertEqual(self.board.__points_status__[5]["count"], 1)

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
        self.assertIn("W:1 B:1", representation)


if __name__ == "__main__":
    unittest.main()
