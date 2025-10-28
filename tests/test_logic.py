# -*- coding: utf-8 -*-
"""
Tests unitarios para la lógica fundamental y funciones de utilidad del juego.

Este archivo contiene tests granulares para funciones específicas que no dependen
directamente de la simulación de eventos de Pygame, sino de la lógica pura del
juego y los cálculos matemáticos.
"""
import unittest
from pygame_ui import main

class TestLogicUtils(unittest.TestCase):
    """
    Suite de tests para la lógica del juego y funciones de utilidad.
    """

    def setUp(self):
        """
        Prepara un estado de juego limpio para cada test.
        """
        # Aunque estos tests son más unitarios, tener un estado de juego
        # disponible puede ser útil para algunas funciones de lógica.
        self.game_data = main.setup_initial_state()

    def test_is_inside_triangle_punto_dentro(self):
        """
        Verifica que la función devuelve True para un punto que está
        claramente dentro de los límites de un triángulo.
        """
        triangulo = [(0, 0), (10, 0), (5, 10)]
        punto_dentro = (5, 5)
        self.assertTrue(main.is_inside_triangle(punto_dentro, triangulo))

    def test_is_inside_triangle_punto_fuera(self):
        """
        Verifica que la función devuelve False para un punto que está
        claramente fuera de los límites de un triángulo.
        """
        triangulo = [(0, 0), (10, 0), (5, 10)]
        punto_fuera = (15, 15)
        # La implementación actual puede dar un falso positivo si el área es negativa,
        # así que nos aseguramos de que el resultado sea explícitamente False.
        self.assertIs(main.is_inside_triangle(punto_fuera, triangulo), False)

    def test_is_inside_triangle_punto_en_vertice(self):
        """
        Verifica que la función devuelve False para un punto que coincide
        exactamente con uno de los vértices del triángulo.
        """
        triangulo = [(0, 0), (10, 0), (5, 10)]
        punto_en_vertice = (0, 0)
        self.assertIs(main.is_inside_triangle(punto_en_vertice, triangulo), False)

    def test_get_opponent_para_blanco(self):
        """
        Verifica que la función devuelve 'B' (Negro) cuando se le pasa
        'W' (Blanco).
        """
        self.assertEqual(main.get_opponent("W"), "B")

    def test_get_opponent_para_negro(self):
        """
        Verifica que la función devuelve 'W' (Blanco) cuando se le pasa
        'B' (Negro).
        """
        self.assertEqual(main.get_opponent("B"), "W")

    def test_can_bear_off_es_posible(self):
        """
        Verifica que can_bear_off devuelve True cuando todas las fichas del
        jugador están en su cuadrante de casa.
        """
        # Preparamos un estado donde todas las fichas blancas están en su casa (puntos 1-6)
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][0] = ["W"] * 5
        self.game_data["board"][2] = ["W"] * 5
        self.game_data["board"][5] = ["W"] * 5
        self.game_data["off"]["W"] = 0
        self.game_data["bar"]["W"] = 0
        self.assertTrue(main.can_bear_off("W", self.game_data))

    def test_can_bear_off_fichas_fuera_de_casa(self):
        """
        Verifica que can_bear_off devuelve False si el jugador todavía tiene
        fichas fuera de su cuadrante de casa.
        """
        # Estado inicial, donde las blancas tienen fichas en los puntos 8 y 13
        self.assertFalse(main.can_bear_off("W", self.game_data))

    def test_can_bear_off_fichas_en_la_barra(self):
        """
        Verifica que can_bear_off devuelve False si el jugador tiene fichas
        en la barra.
        """
        # Preparamos un estado donde todas las fichas están en casa, pero una en la barra
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][0] = ["W"] * 14
        self.game_data["bar"]["W"] = 1
        self.assertFalse(main.can_bear_off("W", self.game_data))

    def test_can_bear_off_oponente_en_casa(self):
        """
        Verifica que can_bear_off devuelve False si una ficha del oponente
        ocupa un punto en el cuadrante de casa del jugador.
        """
        # Todas las fichas blancas en casa, pero una negra en el punto 3
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][0] = ["W"] * 10
        self.game_data["board"][5] = ["W"] * 5
        self.game_data["board"][2] = ["B"]  # Ficha oponente
        self.game_data["bar"]["W"] = 0
        self.assertFalse(main.can_bear_off("W", self.game_data))

    def test_bear_off_regla_exacta(self):
        """
        Verifica que una ficha puede ser retirada si el dado coincide
        exactamente con su número de punto.
        """
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][4] = ["W"]  # Ficha en el punto 5
        self.game_data["off"]["W"] = 14
        dados = [5, 2]

        legal_moves = main.get_legal_moves("W", dados, self.game_data)
        self.assertIn("OFF", legal_moves.get(5, []))

    def test_bear_off_regla_excepcion_overshoot(self):
        """
        Verifica la 'regla de excepción' (overshoot): se puede usar un
        dado de mayor valor para retirar la ficha más lejana si no hay
        otro movimiento posible para ese dado.
        """
        # Fichas Negras en 22 y 23. Dados 4 y 5.
        # No hay movimientos normales ni exactos para estos dados.
        # La ficha más lejana es la del punto 22 (distancia 3 para salir).
        # Ambos dados (4 y 5) son mayores, por lo que se puede usar
        # cualquiera de ellos para sacar la ficha del punto 22.
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][21] = ["B"]  # Punto 22
        self.game_data["board"][22] = ["B"]  # Punto 23
        self.game_data["off"]["B"] = 13
        dados = [4, 5]

        legal_moves = main.get_legal_moves("B", dados, self.game_data)
        self.assertIn("OFF", legal_moves.get(22, []))

    def test_bear_off_excepcion_no_aplica(self):
        """
        Verifica que la regla de excepción no se aplica si existe un
        movimiento válido para ese dado, aunque sea con una ficha más
        adelantada.
        """
        # Fichas Blancas en 6 y 2. Dado de 5.
        # El movimiento del 6 al 1 es válido y tiene prioridad.
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][5] = ["W"]  # Punto 6
        self.game_data["board"][1] = ["W"]  # Punto 2
        self.game_data["off"]["W"] = 13
        dados = [5]

        legal_moves = main.get_legal_moves("W", dados, self.game_data)
        self.assertEqual(legal_moves, {6: [1]})
        self.assertNotIn("OFF", legal_moves.get(2, []))

    def test_bear_off_prioridad_movimiento_normal(self):
        """
        Verifica que un movimiento normal se prioriza sobre un bear-off de
        excepción (overshoot).
        """
        # Fichas Blancas en 5 y 2. Dado de 4. Se debe mover del 5 al 1.
        self.game_data["board"] = [[] for _ in range(24)]
        self.game_data["board"][4] = ["W"]  # Punto 5
        self.game_data["board"][1] = ["W"]  # Punto 2
        self.game_data["off"]["W"] = 13
        dados = [4]

        legal_moves = main.get_legal_moves("W", dados, self.game_data)
        # El único movimiento legal es mover la ficha del 5 al 1.
        # No se debe permitir sacar la ficha del punto 2 con el dado 4.
        self.assertEqual(legal_moves, {5: [1]})


if __name__ == "__main__":
    unittest.main()
