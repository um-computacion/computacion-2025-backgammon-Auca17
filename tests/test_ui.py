# -*- coding: utf-8 -*-
"""
Tests de Interfaz de Usuario (UI) para el juego de Backgammon.

Este archivo contiene tests que simulan interacciones del usuario con la
interfaz de Pygame para verificar que la lógica del juego responde
correctamente a los eventos. Utiliza mocks para simular eventos y el
paso del tiempo sin necesidad de una interacción manual.
"""
import unittest
import unittest.mock
import pygame

from pygame_ui import main


class TestUI(unittest.TestCase):
    """
    Suite de tests para la interfaz de usuario y el flujo de juego.
    """

    def setUp(self):
        """
        Prepara un estado de juego limpio para cada test.
        """
        self.game_data = main.setup_initial_state()
        # Inicializa Pygame en modo sin cabeza (headless) para los tests
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

    def tearDown(self):
        """
        Limpia después de cada test.
        """
        pygame.quit()

    def test_clic_en_boton_jugar_cambia_fase(self):
        """
        Verifica que un clic en el botón 'Jugador vs Jugador' en el menú
        cambia correctamente la fase del juego a 'NAME_INPUT'.
        """
        # 1. Simular la obtención de las coordenadas del botón
        main.draw_menu(None, self.game_data)
        button_rect = self.game_data["buttons"]["vs_player"]

        # 2. Crear un evento de clic simulado en el centro del botón
        mock_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": button_rect.center}
        )

        # 3. Procesar el evento
        self.game_data = main.handle_menu_events(mock_event, self.game_data)

        # 4. Verificar que la fase del juego ha cambiado
        self.assertEqual(self.game_data["game_phase"], "NAME_INPUT")

    def test_clic_fuera_de_boton_no_cambia_fase(self):
        """
        Verifica que un clic fuera del botón 'Jugador vs Jugador' no produce
        ningún cambio en la fase del juego.
        """
        # 1. Simular la obtención de las coordenadas del botón
        main.draw_menu(None, self.game_data)

        # 2. Crear un evento de clic simulado fuera del botón
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})

        # 3. Procesar el evento
        self.game_data = main.handle_menu_events(mock_event, self.game_data)

        # 4. Verificar que la fase del juego NO ha cambiado
        self.assertEqual(self.game_data["game_phase"], "MENU")

    def test_nombres_validos_cambia_fase_a_start_roll(self):
        """
        Verifica que al introducir nombres válidos y pulsar 'Comenzar Partida'
        la fase del juego cambia a 'START_ROLL'.
        """
        # 1. Preparar el estado
        self.game_data["game_phase"] = "NAME_INPUT"
        self.game_data["player_names"]["W"] = "Jugador1"
        self.game_data["player_names"]["B"] = "Jugador2"
        main.draw_name_input(None, self.game_data)
        button_rect = self.game_data["buttons"]["start_game"]

        # 2. Simular clic en el botón de empezar
        mock_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": button_rect.center}
        )

        # 3. Procesar el evento
        self.game_data = main.handle_name_input_events(mock_event, self.game_data)

        # 4. Verificar el cambio de fase
        self.assertEqual(self.game_data["game_phase"], "START_ROLL")
        self.assertTrue(self.game_data["first_roll_data"]["rolled"])

    def test_nombres_invalidos_no_cambia_fase(self):
        """
        Verifica que si los nombres son inválidos (muy cortos), el juego
        no cambia de fase y muestra un mensaje de error.
        """
        self.game_data["game_phase"] = "NAME_INPUT"
        self.game_data["player_names"]["W"] = "J"
        self.game_data["player_names"]["B"] = "Jugador2"
        main.draw_name_input(None, self.game_data)
        button_rect = self.game_data["buttons"]["start_game"]
        mock_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": button_rect.center}
        )

        self.game_data = main.handle_name_input_events(mock_event, self.game_data)

        self.assertEqual(self.game_data["game_phase"], "NAME_INPUT")
        self.assertIn("caracteres", self.game_data["message"])

    def test_escritura_en_input_actualiza_nombre(self):
        """
        Verifica que la simulación de escritura en un campo de texto
        actualiza correctamente el nombre del jugador en el estado del juego.
        """
        self.game_data["game_phase"] = "NAME_INPUT"
        main.draw_name_input(None, self.game_data)  # Para definir las cajas

        # Simular clic para activar el input del jugador 1
        p1_box = self.game_data["input_boxes"]["W"]
        mock_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": p1_box.center})
        self.game_data = main.handle_name_input_events(mock_click, self.game_data)

        # Simular escritura de la letra 'A'
        mock_key_event = pygame.event.Event(
            pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "A"}
        )
        self.game_data = main.handle_name_input_events(mock_key_event, self.game_data)

        self.assertEqual(self.game_data["player_names"]["W"], "A")

    def test_pulsar_espacio_en_start_roll_inicia_partida(self):
        """
        Verifica que al pulsar la barra espaciadora en la fase 'START_ROLL',
        el juego avanza a la fase 'PLAY'.
        """
        # Preparar estado para la tirada inicial
        self.game_data["game_phase"] = "START_ROLL"
        self.game_data["first_roll_data"] = {"W": 6, "B": 4, "rolled": True}
        self.game_data["player_names"] = {"W": "Jugador1", "B": "Jugador2"}

        mock_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})

        self.game_data, _ = main.handle_start_roll_events(
            mock_event, self.game_data, {}
        )

        self.assertEqual(self.game_data["game_phase"], "PLAY")
        self.assertEqual(self.game_data["current_player"], "W")
        self.assertEqual(self.game_data["dice"], [6, 4])

    def test_otras_interacciones_en_start_roll_son_ignoradas(self):
        """
        Verifica que un clic de ratón u otra tecla que no sea espacio son
        ignorados durante la fase 'START_ROLL'.
        """
        self.game_data["game_phase"] = "START_ROLL"
        self.game_data["first_roll_data"] = {"W": 6, "B": 4, "rolled": True}
        initial_state = self.game_data.copy()

        # Simular clic
        mock_mouse_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (100, 100)}
        )
        self.game_data, _ = main.handle_start_roll_events(
            mock_mouse_event, self.game_data, {}
        )
        self.assertEqual(self.game_data["game_phase"], "START_ROLL")

        # Simular otra tecla
        mock_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        self.game_data, _ = main.handle_start_roll_events(
            mock_key_event, self.game_data, {}
        )
        self.assertEqual(self.game_data["game_phase"], "START_ROLL")

    def test_clic_en_ficha_propia_selecciona_punto(self):
        """
        Verifica que al hacer clic en un punto con fichas del jugador actual,
        dicho punto queda marcado como 'selected_point'.
        """
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "B"
        self.game_data["moves_remaining"] = [3, 4]

        # Suponemos que hay un movimiento legal desde el punto 19 para Negras
        legal_moves = {19: [22, 23]}

        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=19
        ):
            mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                mock_event, self.game_data, legal_moves
            )

        self.assertEqual(self.game_data["selected_point"], 19)

    def test_movimiento_valido_actualiza_tablero(self):
        """
        Verifica que un movimiento válido (selección y clic en destino legal)
        actualiza correctamente el estado del tablero.
        """
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "B"
        self.game_data["moves_remaining"] = [3]
        self.game_data["board"][18] = ["B"]  # Ficha en el punto 19
        self.game_data["selected_point"] = 19
        legal_moves = {19: [22]}

        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=22
        ):
            mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                mock_event, self.game_data, legal_moves
            )

        self.assertEqual(len(self.game_data["board"][18]), 0)  # Punto de origen vacío
        self.assertIn("B", self.game_data["board"][21])  # Punto de destino ocupado
        self.assertEqual(len(self.game_data["moves_remaining"]), 0)
        self.assertIsNone(self.game_data["selected_point"])

    def test_movimiento_invalido_no_altera_estado(self):
        """
        Verifica que un clic en un destino no válido no altera el estado del
        juego y simplemente deselecciona el punto.
        """
        self.game_data["game_phase"] = "PLAY"
        self.game_data["current_player"] = "B"
        self.game_data["moves_remaining"] = [3]
        self.game_data["board"][18] = ["B"]
        self.game_data["selected_point"] = 19
        legal_moves = {19: [22]}  # El único destino legal es 22

        initial_board = [p.copy() for p in self.game_data["board"]]

        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value=23
        ):  # Clic en destino no válido
            mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                mock_event, self.game_data, legal_moves
            )

        self.assertEqual(self.game_data["board"], initial_board)
        self.assertIsNone(self.game_data["selected_point"])

    @unittest.mock.patch("pygame_ui.main.is_inside_triangle")
    def test_get_point_from_mouse_identifica_punto_correctamente(self, mock_is_inside):
        """
        Verifica que get_point_from_mouse devuelve el número de punto correcto
        cuando is_inside_triangle devuelve True para ese punto.
        """
        mock_is_inside.side_effect = lambda pos, tri: tri == main.point_positions[12]

        coordenadas_centro_punto_12 = (
            main.point_positions[12][2][0],
            main.point_positions[12][2][1] + 10,
        )

        punto_detectado = main.get_point_from_mouse(coordenadas_centro_punto_12)

        self.assertEqual(punto_detectado, 12)

    def test_get_point_from_mouse_identifica_barra(self):
        """
        Verifica que get_point_from_mouse devuelve 'BAR' para coordenadas
        dentro de la barra central.
        """
        bar_x_start = main.BOARD_MARGIN_X + 6 * main.POINT_WIDTH
        coordenadas_barra = (bar_x_start + main.BAR_WIDTH / 2, main.SCREEN_HEIGHT / 2)

        zona_detectada = main.get_point_from_mouse(coordenadas_barra)

        self.assertEqual(zona_detectada, "BAR")

    def test_get_point_from_mouse_identifica_bear_off(self):
        """
        Verifica que get_point_from_mouse devuelve 'OFF' para coordenadas
        en la zona de bear-off.
        """
        off_x_start = main.SCREEN_WIDTH - main.BOARD_MARGIN_X - main.BEAR_OFF_WIDTH
        coordenadas_off = (off_x_start + 10, main.SCREEN_HEIGHT / 2)

        zona_detectada = main.get_point_from_mouse(coordenadas_off)

        self.assertEqual(zona_detectada, "OFF")

    def test_lanzar_dados_con_espacio(self):
        """
        Verifica que pulsar espacio cuando no hay dados lanza unos nuevos
        y calcula los movimientos legales.
        """
        self.game_data.update(
            {
                "game_phase": "PLAY",
                "current_player": "W",
                "dice": [],
                "moves_remaining": [],
            }
        )

        # Mock para controlar el resultado de los dados
        with unittest.mock.patch("pygame_ui.main.roll_dice", return_value=(3, 4)):
            mock_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
            self.game_data, legal_moves = main.handle_play_events(
                mock_event, self.game_data, {}
            )

        self.assertEqual(self.game_data["dice"], [3, 4])
        self.assertEqual(self.game_data["moves_remaining"], [3, 4])
        self.assertTrue(len(legal_moves) > 0)

    def test_regla_de_dobles_otorga_cuatro_movimientos(self):
        """
        Verifica que si se lanzan dobles, el jugador recibe cuatro
        movimientos del mismo valor.
        """
        self.game_data.update(
            {
                "game_phase": "PLAY",
                "current_player": "W",
                "dice": [],
            }
        )

        with unittest.mock.patch("pygame_ui.main.roll_dice", return_value=(5, 5)):
            mock_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
            self.game_data, _ = main.handle_play_events(mock_event, self.game_data, {})

        self.assertEqual(self.game_data["moves_remaining"], [5, 5, 5, 5])

    def test_condicion_de_victoria_cambia_fase_a_game_over(self):
        """
        Verifica que cuando un jugador ha retirado sus 15 fichas, la fase
        del juego cambia a 'GAME_OVER'.
        """
        self.game_data.update(
            {
                "game_phase": "PLAY",
                "current_player": "W",
                "off": {"W": 14, "B": 0},
                "board": [["W"], *[[] for _ in range(23)]],  # Ficha en el punto 1
                "moves_remaining": [1],
                "selected_point": 1,
            }
        )
        legal_moves = {1: ["OFF"]}

        with unittest.mock.patch(
            "pygame_ui.main.get_point_from_mouse", return_value="OFF"
        ):
            mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                mock_event, self.game_data, legal_moves
            )

        # La victoria se comprueba en el bucle principal, no en el manejador de eventos
        self.game_data = main.check_for_win(self.game_data)

        self.assertEqual(self.game_data["off"]["W"], 15)
        self.assertEqual(self.game_data["game_phase"], "GAME_OVER")

    def test_finalizar_turno_cambia_jugador(self):
        """
        Verifica que después de usar el último movimiento, el turno cambia
        al oponente.
        """
        self.game_data.update(
            {
                "game_phase": "PLAY",
                "current_player": "W",
                "board": [*[[] for _ in range(6)], ["W"], *[[] for _ in range(17)]],
                "moves_remaining": [1],
                "selected_point": 7,
            }
        )
        legal_moves = {7: [6]}

        with unittest.mock.patch("pygame_ui.main.get_point_from_mouse", return_value=6):
            mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (0, 0)})
            self.game_data, _ = main.handle_play_events(
                mock_event, self.game_data, legal_moves
            )
        self.assertEqual(self.game_data["current_player"], "B")
        self.assertEqual(self.game_data["dice"], [])
        self.assertEqual(self.game_data["moves_remaining"], [])


if __name__ == "__main__":
    unittest.main()
