# -*- coding: utf-8 -*-
"""
Tests para la interfaz gráfica (UI) de Backgammon en Pygame.

Este archivo contiene los tests unitarios para verificar el comportamiento de la
interfaz de usuario, simulando eventos y comprobando las transiciones de estado
y las respuestas a las interacciones del usuario.
"""
import unittest
from unittest.mock import patch
import sys
import os
import pygame

# Añade el directorio raíz del proyecto al sys.path
# para permitir importaciones relativas desde la carpeta de tests.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pygame_ui import main


class TestUI(unittest.TestCase):
    """
    Suite de tests para la interfaz de usuario del juego Backgammon.
    """

    def setUp(self):
        """
        Prepara el entorno para cada test.
        Se ejecuta antes de cada método de prueba, asegurando un estado limpio.
        """
        # Inicializa Pygame en un modo no gráfico si es posible,
        # aunque para estos tests no se renderizará nada.
        pygame.init()
        # Restablece el estado del juego a su configuración inicial.
        self.game_data = main.setup_initial_state()

    def tearDown(self):
        """
        Limpia el entorno después de cada test.
        """
        pygame.quit()

    def test_clic_en_boton_jugar_cambia_fase(self):
        """
        Verifica que un clic en el botón 'Jugador vs Jugador' en el menú
        principal cambia la fase del juego a 'NAME_INPUT'.
        """
        # Simula el dibujado del menú para definir el área del botón
        # No se necesita una superficie real (`screen`) porque solo queremos el Rect
        main.draw_menu(None, self.game_data)

        # El centro del botón es un punto seguro para simular el clic
        button_rect = self.game_data["buttons"]["vs_player"]
        pos_centro_boton = button_rect.center

        # Simula un evento de clic del ratón en la posición del botón
        evento_clic = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": pos_centro_boton}
        )

        # Procesa el evento usando la función de manejo de eventos del menú
        self.game_data = main.handle_menu_events(evento_clic, self.game_data)

        # Comprueba que la fase del juego ha cambiado como se esperaba
        self.assertEqual(self.game_data["game_phase"], "NAME_INPUT")

    def test_clic_fuera_de_boton_no_cambia_fase(self):
        """
        Verifica que un clic fuera del botón 'Jugador vs Jugador' no produce
        ningún cambio en la fase del juego.
        """
        # Simula el dibujado para definir el área del botón
        main.draw_menu(None, self.game_data)

        # Elige una posición garantizada fuera de cualquier botón (esquina superior izquierda)
        pos_fuera_boton = (0, 0)

        # Simula el evento de clic
        evento_clic = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": pos_fuera_boton}
        )

        # Procesa el evento
        self.game_data = main.handle_menu_events(evento_clic, self.game_data)

        # Comprueba que la fase del juego sigue siendo 'MENU'
        self.assertEqual(self.game_data["game_phase"], "MENU")

    def test_nombres_validos_cambia_fase_a_start_roll(self):
        """
        Verifica que al introducir nombres válidos y pulsar 'Comenzar Partida'
        la fase del juego cambia a 'START_ROLL'.
        """
        self.game_data["game_phase"] = "NAME_INPUT"
        self.game_data["player_names"]["W"] = "Valido"
        self.game_data["player_names"]["B"] = "Valido2"

        main.draw_name_input(None, self.game_data)
        button_pos = self.game_data["buttons"]["start_game"].center

        evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": button_pos})
        self.game_data = main.handle_name_input_events(evento_clic, self.game_data)

        self.assertEqual(self.game_data["game_phase"], "START_ROLL")

    def test_nombres_invalidos_no_cambia_fase(self):
        """
        Verifica que si los nombres son inválidos (muy cortos), el juego
        no avanza de fase y muestra un mensaje de error.
        """
        self.game_data["game_phase"] = "NAME_INPUT"
        self.game_data["player_names"]["W"] = "a"  # Inválido
        self.game_data["player_names"]["B"] = "JugadorB"

        main.draw_name_input(None, self.game_data)
        button_pos = self.game_data["buttons"]["start_game"].center

        evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": button_pos})
        self.game_data = main.handle_name_input_events(evento_clic, self.game_data)

        self.assertEqual(self.game_data["game_phase"], "NAME_INPUT")
        self.assertIn("caracteres", self.game_data["message"])

    def test_escritura_en_input_actualiza_nombre(self):
        """
        Verifica que la simulación de escritura en un campo de texto
        actualiza correctamente el nombre del jugador en el estado del juego.
        """
        self.game_data["game_phase"] = "NAME_INPUT"
        main.draw_name_input(None, self.game_data)  # Para definir las cajas

        # 1. Simular clic para activar el input del jugador blanco
        input_box_pos = self.game_data["input_boxes"]["W"].center
        evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": input_box_pos})
        self.game_data = main.handle_name_input_events(evento_clic, self.game_data)
        self.assertEqual(self.game_data["active_input"], "W")

        # 2. Simular escritura de la letra 'A'
        # Se añade un 'key' para evitar el AttributeError, aunque no se use para la 'A'.
        evento_tecla = pygame.event.Event(
            pygame.KEYDOWN, {"unicode": "A", "key": pygame.K_a}
        )
        self.game_data = main.handle_name_input_events(evento_tecla, self.game_data)

        self.assertEqual(self.game_data["player_names"]["W"], "A")

    def test_pulsar_espacio_en_start_roll_inicia_partida(self):
        """
        Verifica que al pulsar la barra espaciadora en la fase 'START_ROLL',
        el juego avanza a la fase 'PLAY' y se asigna el turno correctamente.
        """
        self.game_data["game_phase"] = "START_ROLL"
        # Simulamos datos de una tirada inicial donde gana el jugador Blanco
        self.game_data["first_roll_data"] = {"W": 6, "B": 1, "rolled": True}
        self.game_data["player_names"] = {"W": "P1", "B": "P2"}

        legal_moves = {}
        evento_espacio = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})

        self.game_data, legal_moves = main.handle_start_roll_events(
            evento_espacio, self.game_data, legal_moves
        )

        self.assertEqual(self.game_data["game_phase"], "PLAY")
        self.assertEqual(self.game_data["current_player"], "W")
        self.assertTrue(legal_moves)  # Deben haberse calculado movimientos legales

    def test_otras_interacciones_en_start_roll_son_ignoradas(self):
        """
        Verifica que un clic de ratón u otra tecla que no sea espacio son
        ignorados durante la fase 'START_ROLL'.
        """
        self.game_data["game_phase"] = "START_ROLL"
        self.game_data["first_roll_data"] = {"W": 6, "B": 1, "rolled": True}

        estado_original = self.game_data.copy()
        legal_moves = {}

        # Simular un clic de ratón
        evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (1, 1)})
        self.game_data, legal_moves = main.handle_start_roll_events(
            evento_clic, self.game_data, legal_moves
        )

        # Simular pulsación de otra tecla (ej. 'a')
        evento_tecla_a = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        self.game_data, legal_moves = main.handle_start_roll_events(
            evento_tecla_a, self.game_data, legal_moves
        )

        self.assertEqual(self.game_data, estado_original)
        self.assertFalse(legal_moves)

    def test_clic_en_ficha_propia_selecciona_punto(self):
        """
        Verifica que al hacer clic en un punto con fichas del jugador actual,
        el estado 'selected_point' se actualiza correctamente.
        """
        # Configuración inicial para el test
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "W"
        self.game_data["dice"] = [3, 4]
        self.game_data["moves_remaining"] = [3, 4]
        # El jugador 'W' tiene una ficha en el punto 24 (índice 23)
        self.game_data["board"][23] = ["W"]

        legal_moves = main.get_legal_moves("W", [3, 4], self.game_data)

        # Simula un clic en el punto 24
        # Nota: get_point_from_mouse devuelve el número de punto (1-24), no el índice
        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=24
        ):
            evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                evento_clic, self.game_data, legal_moves
            )

        self.assertEqual(self.game_data["selected_point"], 24)

    def test_movimiento_valido_actualiza_tablero(self):
        """
        Verifica que un movimiento válido (selección y clic en destino legal)
        actualiza correctamente el tablero y consume un movimiento.
        """
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "W"
        self.game_data["board"][23] = ["W"]  # Ficha en punto 24
        self.game_data["dice"] = [3, 4]
        self.game_data["moves_remaining"] = [3, 4]
        self.game_data["selected_point"] = 24  # Punto ya seleccionado

        legal_moves = main.get_legal_moves("W", [3, 4], self.game_data)

        # Simula un clic en el destino legal (24 - 3 = punto 21)
        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=21
        ):
            evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                evento_clic, self.game_data, legal_moves
            )

        self.assertEqual(len(self.game_data["board"][23]), 0)  # Punto de origen vacío
        self.assertEqual(self.game_data["board"][20], ["W"])  # Punto de destino ocupado
        self.assertNotIn(3, self.game_data["moves_remaining"])  # Dado consumido

    def test_movimiento_invalido_no_altera_estado(self):
        """
        Verifica que un clic en un destino no válido no altera el estado del
        juego (tablero, movimientos, etc.).
        """
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "W"
        self.game_data["board"][23] = ["W"]
        self.game_data["dice"] = [3, 4]
        self.game_data["moves_remaining"] = [3, 4]
        self.game_data["selected_point"] = 24

        estado_original = self.game_data.copy()
        legal_moves = main.get_legal_moves("W", [3, 4], self.game_data)

        # Simula clic en un punto no legal (ej. 23)
        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=23
        ):
            evento_clic = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                evento_clic, self.game_data, legal_moves
            )

        self.assertEqual(self.game_data["board"], estado_original["board"])
        self.assertEqual(
            self.game_data["moves_remaining"], estado_original["moves_remaining"]
        )


if __name__ == "__main__":
    unittest.main()
