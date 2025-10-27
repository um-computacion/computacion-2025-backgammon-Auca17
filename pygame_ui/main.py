# -*- coding: utf-8 -*-
"""
Juego de Backgammon con Pygame

Este archivo contiene la implementación completa del juego de Backgammon
utilizando la librería Pygame. Todo el código, desde la lógica del juego
hasta la interfaz gráfica, se encuentra en este único archivo para
simplificar la distribución y la lectura.

Estructura del Archivo:
-----------------------
1.  **Imports y Constantes**:
    Se importan las librerías necesarias y se definen las constantes
    globales como colores, dimensiones de la ventana, tamaños de fuente y
    geometría del tablero.

2.  **Modelo de Datos (Estado del Juego)**:
    Aquí se definen las estructuras de datos que representan el estado del
    juego en memoria, incluyendo la disposición de las fichas en el
    tablero, la barra y las fichas retiradas.

3.  **Funciones de Lógica del Juego**:
    Contiene las funciones que implementan las reglas del Backgammon:
    -   Tirar los dados.
    -   Validar movimientos.
    -   Gestionar el reingreso desde la barra.
    -   Gestionar el bear-off (retirada de fichas).
    -   Controlar el flujo de turnos.

4.  **Funciones de Dibujo (Renderizado)**:
    Funciones responsables de dibujar todos los elementos gráficos en la
    pantalla: el tablero, las fichas, el HUD (Heads-Up Display) y los
    resaltados visuales para guiar al jugador.

5.  **Manejo de Input del Usuario**:
    Se gestionan los eventos de Pygame, como clics del ratón y pulsaciones
    de teclas, para traducir las acciones del jugador en cambios en el

6.  **Bucle Principal del Juego**:
    El `main loop` que mantiene el juego en funcionamiento, procesando
    eventos, actualizando el estado y redibujando la pantalla en cada
    frame.
"""

import pygame
import sys
import random

# --- 1. Imports y Constantes -----------------------------------------------

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Backgammon")

# Colores (RGB)
COLOR_BOARD = (210, 180, 140)  # Un color madera claro para el tablero
COLOR_POINT_A = (128, 0, 0)  # Triángulos de color vino
COLOR_POINT_B = (0, 0, 0)  # Triángulos negros
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (20, 20, 20)
COLOR_HIGHLIGHT = (255, 255, 0, 100)  # Amarillo semitransparente para resaltar
COLOR_HUD_BG = (100, 100, 100)
COLOR_HUD_TEXT = (240, 240, 240)
COLOR_MENU_BG = (245, 245, 245)
COLOR_BUTTON_PRIMARY = (85, 85, 85)
COLOR_TEXT_DARK = (0, 0, 0)  # Negro para máximo contraste
COLOR_BRICK = (140, 140, 140)  # Un tono de gris para el ladrillo
COLOR_MORTAR = (184, 173, 173)  # Un gris claro para las juntas


# Fuentes
font_title = pygame.font.SysFont("Arial", 48, bold=True)
font_hud = pygame.font.SysFont("Arial", 24)
font_hud_bold = pygame.font.SysFont("Arial", 24, bold=True)
font_message = pygame.font.SysFont("Arial", 28, bold=True)
font_point_num = pygame.font.SysFont("Arial", 18, bold=True)
font_small = pygame.font.SysFont("Arial", 16)
font_small_bold = pygame.font.SysFont("Arial", 16, bold=True)


# Geometría del tablero
HUD_TOP_MARGIN = 10
HUD_HEIGHT = 60
BOARD_MARGIN_X = 20
BOARD_MARGIN_Y = 30
BEAR_OFF_WIDTH = 60
BOARD_BEAR_OFF_GAP = 20  # Espacio entre el tablero y la zona de bear-off
BAR_WIDTH = 70

BOARD_TOP_Y = HUD_TOP_MARGIN + HUD_HEIGHT
BOARD_BOTTOM_Y = SCREEN_HEIGHT - BOARD_MARGIN_Y
BOARD_PLAY_HEIGHT = BOARD_BOTTOM_Y - BOARD_TOP_Y

# El ancho total del tablero de juego
GAME_AREA_WIDTH = (
    SCREEN_WIDTH - 2 * BOARD_MARGIN_X - BEAR_OFF_WIDTH - BOARD_BEAR_OFF_GAP
)
POINT_WIDTH = (GAME_AREA_WIDTH - BAR_WIDTH) / 12
POINT_HEIGHT = (
    BOARD_PLAY_HEIGHT * 0.4
)  # Triángulos más cortos para dar espacio a los números

# Posiciones de los puntos (triángulos)
point_positions = {}
for i in range(12):
    x_base = BOARD_MARGIN_X + i * POINT_WIDTH
    if i >= 6:
        x_base += BAR_WIDTH
    # Puntos de abajo (1 a 12)
    point_positions[12 - i] = [
        (x_base, BOARD_BOTTOM_Y),
        (x_base + POINT_WIDTH, BOARD_BOTTOM_Y),
        (x_base + POINT_WIDTH / 2, BOARD_BOTTOM_Y - POINT_HEIGHT),
    ]
    # Puntos de arriba (24 a 13)
    point_positions[13 + i] = [
        (x_base, BOARD_TOP_Y),
        (x_base + POINT_WIDTH, BOARD_TOP_Y),
        (x_base + POINT_WIDTH / 2, BOARD_TOP_Y + POINT_HEIGHT),
    ]

# --- 2. Modelo de Datos (Estado del Juego) ---------------------------------

# Identificadores para los jugadores
PLAYER_WHITE = "W"
PLAYER_BLACK = "B"


def setup_initial_state():
    """
    Configura y devuelve el estado inicial completo del juego.

    Esto incluye la posición de las fichas en el tablero, la barra, las fichas
    retiradas y el estado general del juego como el turno y los dados.
    """
    # El tablero se representa como una lista de 24 listas. Cada sublista
    # representa un punto y contiene las fichas (ej. ['W', 'W']).
    # El índice 0 corresponde al punto 1, y el índice 23 al punto 24.
    board = [[] for _ in range(24)]

    # Posición inicial estándar del Backgammon
    board[0] = [PLAYER_BLACK] * 2  # Punto 1
    board[5] = [PLAYER_WHITE] * 5  # Punto 6
    board[7] = [PLAYER_WHITE] * 3  # Punto 8
    board[11] = [PLAYER_BLACK] * 5  # Punto 12
    board[12] = [PLAYER_WHITE] * 5  # Punto 13
    board[16] = [PLAYER_BLACK] * 3  # Punto 17
    board[18] = [PLAYER_BLACK] * 5  # Punto 19
    board[23] = [PLAYER_WHITE] * 2  # Punto 24

    # Fichas en la barra (inicialmente vacía para ambos jugadores)
    bar = {PLAYER_WHITE: 0, PLAYER_BLACK: 0}

    # Fichas retiradas (bear-off, inicialmente cero para ambos)
    off = {PLAYER_WHITE: 0, PLAYER_BLACK: 0}

    # Diccionario principal que encapsula todo el estado del juego
    game_state = {
        "board": board,
        "bar": bar,
        "off": off,
        "current_player": None,  # Se decide con la primera tirada
        "dice": [],  # ej: [4, 5]
        "moves_remaining": [],  # Movimientos disponibles según los dados
        "selected_point": None,
        "message": "Bienvenido a Backgammon",
        "game_phase": "MENU",  # Fases: MENU, NAME_INPUT, START_ROLL, PLAY, GAME_OVER
        "player_names": {PLAYER_WHITE: "", PLAYER_BLACK: ""},
        "active_input": None,
        "input_boxes": {},
        "buttons": {},
        "first_roll_data": {PLAYER_WHITE: 0, PLAYER_BLACK: 0, "rolled": False},
    }
    return game_state


# Se inicializa el estado del juego al arrancar el programa
game_data = setup_initial_state()


# --- 3. Funciones de Lógica del Juego --------------------------------------


def roll_dice():
    """
    Lanza dos dados y devuelve una tupla con los resultados.
    """
    return (random.randint(1, 6), random.randint(1, 6))


def get_opponent(player):
    """
    Devuelve el identificador del jugador oponente.
    """
    return PLAYER_BLACK if player == PLAYER_WHITE else PLAYER_WHITE


def can_bear_off(player, game_state):
    """
    Verifica si un jugador puede empezar a retirar fichas (bear-off).
    Condiciones:
    1. Todas las 15 fichas del jugador deben estar en su cuadrante de casa.
    - Casa de Blancas (W): puntos 1-6 (índices 0-5).
    - Casa de Negras (B): puntos 19-24 (índices 18-23).
    """
    board = game_state["board"]
    if game_state["bar"][player] > 0:
        return False  # No se puede hacer bear-off con fichas en la barra.

    home_board_indices = range(0, 6) if player == PLAYER_WHITE else range(18, 24)
    opponent = get_opponent(player)
    checkers_in_home = 0

    for i in home_board_indices:
        # Si hay una ficha del oponente en el cuadrante, no se puede retirar.
        if board[i] and board[i][0] == opponent:
            return False
        if board[i] and board[i][0] == player:
            checkers_in_home += len(board[i])

    # El total de fichas en casa más las retiradas debe ser 15.
    return checkers_in_home + game_state["off"][player] == 15


def get_legal_moves(player, dice, game_state):
    """
    Encuentra todos los movimientos legales para un jugador dados los resultados de los dados.
    Devuelve un diccionario donde las claves son los puntos de origen y los valores
    son listas de posibles puntos de destino.
    """
    legal_moves = {}
    board = game_state["board"]

    # --- Regla 1: Reingreso desde la barra ---
    if game_state["bar"][player] > 0:
        for die in set(dice):
            # El destino se calcula desde un "punto 0" o "punto 25" conceptual.
            if player == PLAYER_WHITE:
                target_point_idx = 24 - die
            else:  # PLAYER_BLACK
                target_point_idx = die - 1

            # Comprobar si el punto de entrada está bloqueado
            if (
                len(board[target_point_idx]) <= 1
                or board[target_point_idx][0] == player
            ):
                if "BAR" not in legal_moves:
                    legal_moves["BAR"] = []
                legal_moves["BAR"].append(target_point_idx + 1)
        return legal_moves  # Si hay fichas en la barra, no se pueden hacer otros movimientos

    # --- Regla 2: Movimientos normales y Bear-off ---
    can_do_bear_off = can_bear_off(player, game_state)

    for point_idx, checkers in enumerate(board):
        if checkers and checkers[0] == player:
            start_point = point_idx + 1

            for die in set(dice):
                if player == PLAYER_WHITE:
                    target_point_idx = point_idx - die
                else:  # PLAYER_BLACK
                    target_point_idx = point_idx + die

                # Movimiento normal dentro del tablero
                if 0 <= target_point_idx < 24:
                    if (
                        len(board[target_point_idx]) <= 1
                        or board[target_point_idx][0] == player
                    ):
                        if start_point not in legal_moves:
                            legal_moves[start_point] = []
                        legal_moves[start_point].append(target_point_idx + 1)

                # Bear-off
                elif can_do_bear_off:
                    if player == PLAYER_WHITE and target_point_idx < 0:
                        # Regla exacta: la ficha está en el punto que marca el dado
                        if start_point == die:
                            if start_point not in legal_moves:
                                legal_moves[start_point] = []
                            legal_moves[start_point].append("OFF")
                        # Regla de excedente
                        else:
                            # Regla de excedente: solo se puede usar un dado mayor si no hay
                            # fichas en puntos más altos.
                            is_further_checker = False
                            for p in range(
                                start_point + 1, 7
                            ):  # Para blancas, puntos más altos son 6, 5, 4...
                                if board[p - 1] and board[p - 1][0] == player:
                                    is_further_checker = True
                                    break
                            if not is_further_checker and die > start_point:
                                if start_point not in legal_moves:
                                    legal_moves[start_point] = []
                                legal_moves[start_point].append("OFF")

                    elif player == PLAYER_BLACK and target_point_idx >= 24:
                        # Regla exacta
                        if (25 - start_point) == die:
                            if start_point not in legal_moves:
                                legal_moves[start_point] = []
                            legal_moves[start_point].append("OFF")
                        # Regla de excedente
                        else:
                            is_further_checker = False
                            for p in range(
                                start_point - 1, 18, -1
                            ):  # Para negras, puntos más altos son 19, 20...
                                if board[p - 1] and board[p - 1][0] == player:
                                    is_further_checker = True
                                    break
                            if not is_further_checker and die > (25 - start_point):
                                if start_point not in legal_moves:
                                    legal_moves[start_point] = []
                                legal_moves[start_point].append("OFF")
    return legal_moves


def apply_move(start_point, end_point, player, game_state):
    """
    Aplica un movimiento al estado del juego.
    start_point puede ser un número (1-24) o 'BAR'.
    end_point puede ser un número (1-24) o 'OFF'.
    """
    board = game_state["board"]
    opponent = get_opponent(player)

    # 1. Quitar ficha del origen
    if start_point == "BAR":
        game_state["bar"][player] -= 1
    else:
        board[start_point - 1].pop()

    # 2. Añadir ficha al destino
    if end_point == "OFF":
        game_state["off"][player] += 1
    else:
        target_idx = end_point - 1
        # Comprobar si se come una ficha rival (blot)
        if board[target_idx] and board[target_idx][0] == opponent:
            board[target_idx].pop()
            game_state["bar"][opponent] += 1
            game_state["message"] = (
                f"{'Negras' if opponent == 'B' else 'Blancas'} a la barra!"
            )
        board[target_idx].append(player)

    return game_state


# --- 4. Funciones de Dibujo (Renderizado) ----------------------------------


def draw_brick_background(surface):
    """Dibuja un fondo de pared de ladrillos de estilo medieval."""
    brick_width = 80
    brick_height = 40
    mortar_thickness = 4

    # Rellena todo el fondo con el color del mortero
    surface.fill(COLOR_MORTAR)

    for y in range(0, SCREEN_HEIGHT, brick_height):
        # Desplaza cada segunda fila para crear el patrón de ladrillo
        offset = (y // brick_height) % 2 * (brick_width // 2)
        for x in range(-offset, SCREEN_WIDTH, brick_width):
            brick_rect = pygame.Rect(
                x + mortar_thickness // 2,
                y + mortar_thickness // 2,
                brick_width - mortar_thickness,
                brick_height - mortar_thickness,
            )
            pygame.draw.rect(surface, COLOR_BRICK, brick_rect, border_radius=4)


def draw_board(surface):
    """
    Dibuja el tablero de Backgammon, incluyendo los puntos (triángulos) y la barra.
    """
    # Primero, el fondo de ladrillos para toda la pantalla
    draw_brick_background(surface)

    # Luego, el rectángulo de madera que representa el tablero
    board_rect = pygame.Rect(
        BOARD_MARGIN_X, BOARD_TOP_Y, GAME_AREA_WIDTH, BOARD_PLAY_HEIGHT
    )
    pygame.draw.rect(surface, COLOR_BOARD, board_rect)

    # Dibuja los 24 puntos (triángulos) sobre el tablero
    for i in range(1, 25):
        color = COLOR_POINT_A if (i % 2) != 0 else COLOR_POINT_B
        if 1 <= i <= 6 or 13 <= i <= 18:
            color = COLOR_POINT_B if (i % 2) != 0 else COLOR_POINT_A
        pygame.draw.polygon(surface, color, point_positions[i])

    # Dibuja la barra central
    bar_x = BOARD_MARGIN_X + 6 * POINT_WIDTH
    pygame.draw.rect(
        surface, (0, 0, 0, 50), (bar_x, BOARD_TOP_Y, BAR_WIDTH, BOARD_PLAY_HEIGHT)
    )

    # Dibuja los números de los puntos
    for i in range(1, 25):
        text = font_point_num.render(str(i), True, COLOR_BLACK)
        x_pos = point_positions[i][2][0] - text.get_width() / 2

        # Centra los números en el espacio creado en medio del tablero
        y_center = BOARD_TOP_Y + BOARD_PLAY_HEIGHT / 2
        text_height = text.get_height()
        padding = (
            30  # Aumentado para que los números no se solapen con la barra de mensajes
        )

        if i > 12:  # Puntos de arriba (13-24), números justo encima de la línea central
            y_pos = y_center - padding - text_height
        else:  # Puntos de abajo (1-12), números justo debajo de la línea central
            y_pos = y_center + padding
        surface.blit(text, (x_pos, y_pos))


def draw_checker(surface, body_color, center, radius):
    """Dibuja una ficha de color sólido con un borde para un look más limpio."""
    border_width = 3

    if body_color == COLOR_WHITE:
        border_color = (180, 180, 180)  # Gris claro
    else:  # COLOR_BLACK
        border_color = (70, 70, 70)  # Gris oscuro

    # Dibuja el cuerpo de la ficha
    pygame.draw.circle(surface, body_color, center, radius)
    # Dibuja el borde encima
    pygame.draw.circle(surface, border_color, center, radius, border_width)


def draw_decorative_banner(surface):
    """
    Dibuja una guirnalda decorativa de banderines en la parte superior.
    """
    # --- Parámetros de la guirnalda ---
    y_start = 20  # Subimos un poco la guirnalda
    sag = 30  # Caída de la cuerda en el centro (positiva para ir hacia abajo)
    num_banners = 15  # Aumentado para cubrir más espacio
    banner_width = 45
    banner_height = 55
    rope_color = COLOR_TEXT_DARK
    rope_thickness = 3
    shadow_offset = 3
    shadow_color = (0, 0, 0, 120)  # Color de sombra (no usado directamente por ahora)
    shadow_draw_color = (40, 40, 40)  # Un gris oscuro para la sombra

    # La cuerda ahora va de extremo a extremo
    x_start = 0
    x_end = SCREEN_WIDTH

    # --- Dibujar la cuerda con la gravedad correcta ---
    points = []
    num_segments = 50
    for i in range(num_segments + 1):
        x = x_start + i * (x_end - x_start) / num_segments
        # Se invierte el signo de 'sag' para que la curva vaya hacia abajo
        y = (-4 * sag / ((x_end - x_start) ** 2)) * (x - x_start) * (
            x - x_end
        ) + y_start
        points.append((x, y))
    pygame.draw.lines(surface, rope_color, False, points, rope_thickness)

    # --- Dibujar las sombras primero ---
    for i in range(num_banners):
        x_center = (
            x_start
            + (banner_width / 2)
            + i * (x_end - x_start - banner_width) / (num_banners - 1)
        )
        y_rope = (-4 * sag / ((x_end - x_start) ** 2)) * (x_center - x_start) * (
            x_center - x_end
        ) + y_start

        # Vértices de la sombra (ligeramente desplazados)
        s_p1 = (x_center - banner_width / 2 + shadow_offset, y_rope + shadow_offset)
        s_p2 = (x_center + banner_width / 2 + shadow_offset, y_rope + shadow_offset)
        s_p3 = (x_center + shadow_offset, y_rope + banner_height + shadow_offset)
        pygame.draw.polygon(surface, shadow_draw_color, [s_p1, s_p2, s_p3])

    # --- Dibujar los banderines encima de las sombras ---
    for i in range(num_banners):
        x_center = (
            x_start
            + (banner_width / 2)
            + i * (x_end - x_start - banner_width) / (num_banners - 1)
        )
        y_rope = (-4 * sag / ((x_end - x_start) ** 2)) * (x_center - x_start) * (
            x_center - x_end
        ) + y_start

        # Vértices del banderín
        p1 = (x_center - banner_width / 2, y_rope)
        p2 = (x_center + banner_width / 2, y_rope)
        p3 = (x_center, y_rope + banner_height)

        color = COLOR_POINT_A if i % 2 == 0 else COLOR_POINT_B
        pygame.draw.polygon(surface, color, [p1, p2, p3])


def draw_checkers(surface, game_state):
    """
    Dibuja las fichas en el tablero, la barra y la zona de bear-off.
    """
    board = game_state["board"]
    bar = game_state["bar"]
    off = game_state["off"]
    checker_radius = int(POINT_WIDTH * 0.38)  # Fichas ligeramente más pequeñas

    # Dibuja las fichas en los puntos
    for point_idx, checkers in enumerate(board):
        point_num = point_idx + 1
        x_center = point_positions[point_num][2][0]

        for i, checker_color in enumerate(checkers):
            color = COLOR_WHITE if checker_color == PLAYER_WHITE else COLOR_BLACK

            if point_num <= 12:  # Puntos de abajo
                y_pos = BOARD_BOTTOM_Y - checker_radius - (i * (checker_radius * 2))
            else:  # Puntos de arriba
                y_pos = BOARD_TOP_Y + checker_radius + (i * (checker_radius * 2))

            # Si hay más de 5 fichas, se muestra un contador
            if i >= 5:  # A partir de la 6ta ficha
                y_pos_last = (
                    BOARD_BOTTOM_Y - checker_radius - (4 * (checker_radius * 2))
                    if point_num <= 12
                    else BOARD_TOP_Y + checker_radius + (4 * (checker_radius * 2))
                )
                # Dibuja la 5ta ficha
                draw_checker(surface, color, (x_center, y_pos_last), checker_radius)
                # Dibuja el contador encima
                count_text = font_hud.render(
                    f"x{len(checkers)}",
                    True,
                    COLOR_HIGHLIGHT if color == COLOR_BLACK else COLOR_BLACK,
                )
                surface.blit(
                    count_text,
                    (
                        x_center - count_text.get_width() / 2,
                        y_pos_last - count_text.get_height() / 2,
                    ),
                )
                break

            draw_checker(surface, color, (x_center, y_pos), checker_radius)

    # Dibuja las fichas en la barra
    bar_x = BOARD_MARGIN_X + 6 * POINT_WIDTH + BAR_WIDTH / 2
    for i in range(bar[PLAYER_WHITE]):
        y_pos = BOARD_BOTTOM_Y - checker_radius - (i * (checker_radius * 2))
        draw_checker(surface, COLOR_WHITE, (bar_x, y_pos), checker_radius)
    for i in range(bar[PLAYER_BLACK]):
        y_pos = BOARD_TOP_Y + checker_radius + (i * (checker_radius * 2))
        draw_checker(surface, COLOR_BLACK, (bar_x, y_pos), checker_radius)

    # Dibuja los contadores de bear-off en la nueva columna derecha
    off_area_x = SCREEN_WIDTH - BOARD_MARGIN_X - BEAR_OFF_WIDTH + 5
    off_area_h = BOARD_PLAY_HEIGHT / 2 - 20
    checker_radius_off = int((BEAR_OFF_WIDTH - 10) * 0.3)  # Radio para la ficha pequeña

    # --- Área para Negras (arriba) ---
    off_area_b = pygame.Rect(off_area_x, BOARD_TOP_Y, BEAR_OFF_WIDTH - 10, off_area_h)
    pygame.draw.rect(surface, COLOR_HUD_BG, off_area_b, border_radius=8)

    # Renderizar y posicionar número
    off_text_b = font_message.render(str(off[PLAYER_BLACK]), True, COLOR_WHITE)
    text_b_center_y = off_area_b.y + off_area_b.height * 0.35
    surface.blit(
        off_text_b,
        (
            off_area_b.centerx - off_text_b.get_width() / 2,
            text_b_center_y - off_text_b.get_height() / 2,
        ),
    )

    # Posicionar ficha indicadora
    checker_b_center = (off_area_b.centerx, off_area_b.y + off_area_b.height * 0.75)
    draw_checker(surface, COLOR_BLACK, checker_b_center, checker_radius_off)

    # --- Área para Blancas (abajo) ---
    off_area_w = pygame.Rect(
        off_area_x,
        BOARD_TOP_Y + BOARD_PLAY_HEIGHT / 2 + 10,
        BEAR_OFF_WIDTH - 10,
        off_area_h,
    )
    pygame.draw.rect(surface, COLOR_HUD_BG, off_area_w, border_radius=8)

    # Renderizar y posicionar número
    off_text_w = font_message.render(str(off[PLAYER_WHITE]), True, COLOR_WHITE)
    text_w_center_y = off_area_w.y + off_area_w.height * 0.35
    surface.blit(
        off_text_w,
        (
            off_area_w.centerx - off_text_w.get_width() / 2,
            text_w_center_y - off_text_w.get_height() / 2,
        ),
    )

    # Posicionar ficha indicadora
    checker_w_center = (off_area_w.centerx, off_area_w.y + off_area_w.height * 0.75)
    draw_checker(surface, COLOR_WHITE, checker_w_center, checker_radius_off)


def draw_menu(surface, game_state):
    """
    Dibuja el menú principal. Si 'surface' es None, solo actualiza
    el estado del juego (ej. 'buttons') sin renderizar.
    """
    button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 50, 300, 60)
    game_state["buttons"]["vs_player"] = button_rect

    if surface is None:
        return  # Modo de prueba: solo registrar componentes, no dibujar.

    draw_brick_background(surface)
    draw_decorative_banner(surface)

    # Título
    title_text = font_title.render("Backgammon", True, COLOR_TEXT_DARK)
    surface.blit(
        title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, SCREEN_HEIGHT / 3)
    )

    # Botón con fondo blanco y borde negro para mejor contraste
    pygame.draw.rect(surface, COLOR_WHITE, button_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_TEXT_DARK, button_rect, 2, border_radius=15)

    button_text = font_hud_bold.render("Jugador vs Jugador", True, COLOR_TEXT_DARK)
    surface.blit(
        button_text,
        (
            button_rect.centerx - button_text.get_width() / 2,
            button_rect.centery - button_text.get_height() / 2,
        ),
    )


def draw_name_input(surface, game_state):
    """
    Dibuja la pantalla de entrada de nombres. Si 'surface' es None,
    solo actualiza el estado del juego (cajas, botones) sin renderizar.
    """
    panel_rect = pygame.Rect(SCREEN_WIDTH / 2 - 250, 260, 500, 350)
    p1_box = pygame.Rect(
        panel_rect.left + 30, panel_rect.top + 65, panel_rect.width - 60, 45
    )
    p2_box = pygame.Rect(
        panel_rect.left + 30, panel_rect.top + 165, panel_rect.width - 60, 45
    )
    start_button = pygame.Rect(
        panel_rect.centerx - 150, panel_rect.bottom - 80, 300, 60
    )

    game_state["input_boxes"][PLAYER_WHITE] = p1_box
    game_state["input_boxes"][PLAYER_BLACK] = p2_box
    game_state["buttons"]["start_game"] = start_button

    if surface is None:
        return  # Modo de prueba

    draw_brick_background(surface)
    draw_decorative_banner(surface)

    title = font_title.render("Configuración de Partida", True, COLOR_TEXT_DARK)
    surface.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 160))

    # --- Input para Jugador 1 ---
    p1_label = font_hud_bold.render("Jugador 1 (Blancas)", True, COLOR_TEXT_DARK)
    surface.blit(p1_label, (panel_rect.left + 30, panel_rect.top + 30))
    pygame.draw.rect(surface, COLOR_WHITE, p1_box, border_radius=10)
    border_color = (
        COLOR_BUTTON_PRIMARY
        if game_state["active_input"] == PLAYER_WHITE
        else COLOR_HUD_BG
    )
    pygame.draw.rect(surface, border_color, p1_box, 2, border_radius=10)
    p1_text = font_hud_bold.render(
        game_state["player_names"][PLAYER_WHITE], True, COLOR_TEXT_DARK
    )
    surface.blit(p1_text, (p1_box.x + 15, p1_box.centery - p1_text.get_height() / 2))

    # --- Input para Jugador 2 ---
    p2_label = font_hud_bold.render("Jugador 2 (Negras)", True, COLOR_TEXT_DARK)
    surface.blit(p2_label, (panel_rect.left + 30, panel_rect.top + 130))
    pygame.draw.rect(surface, COLOR_WHITE, p2_box, border_radius=10)
    border_color_p2 = (
        COLOR_BUTTON_PRIMARY
        if game_state["active_input"] == PLAYER_BLACK
        else COLOR_HUD_BG
    )
    pygame.draw.rect(surface, border_color_p2, p2_box, 2, border_radius=10)
    p2_text = font_hud_bold.render(
        game_state["player_names"][PLAYER_BLACK], True, COLOR_TEXT_DARK
    )
    surface.blit(p2_text, (p2_box.x + 15, p2_box.centery - p2_text.get_height() / 2))

    # --- Texto informativo de caracteres ---
    char_info_text = font_small_bold.render(
        "Mínimo 2, máximo 10 caracteres.", True, COLOR_TEXT_DARK
    )
    surface.blit(char_info_text, (p2_box.left, p2_box.bottom + 10))

    # --- Botón de Comenzar ---

    # Botón con fondo blanco y borde negro para mejor contraste
    pygame.draw.rect(surface, COLOR_WHITE, start_button, border_radius=15)
    pygame.draw.rect(surface, COLOR_TEXT_DARK, start_button, 2, border_radius=15)
    start_text = font_hud_bold.render("Comenzar Partida", True, COLOR_TEXT_DARK)
    surface.blit(
        start_text,
        (
            start_button.centerx - start_text.get_width() / 2,
            start_button.centery - start_text.get_height() / 2,
        ),
    )

    # --- Mensaje de error ---
    if "caracteres" in game_state["message"]:
        error_text = font_message.render(game_state["message"], True, COLOR_POINT_A)
        surface.blit(
            error_text,
            (SCREEN_WIDTH / 2 - error_text.get_width() / 2, panel_rect.bottom + 20),
        )


def draw_dice(surface, value, x, y, size=50):
    """Dibuja un único dado gráfico de tamaño variable."""
    dice_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, COLOR_WHITE, dice_rect, border_radius=int(size * 0.1))

    dot_radius = int(size * 0.1)

    # Las posiciones de los puntos se calculan en base al tamaño del dado
    # Usamos fracciones del tamaño para que escale correctamente.
    s = size  # Abreviatura para claridad
    pos_map = {
        1: [(s * 0.5, s * 0.5)],
        2: [(s * 0.25, s * 0.25), (s * 0.75, s * 0.75)],
        3: [(s * 0.25, s * 0.25), (s * 0.5, s * 0.5), (s * 0.75, s * 0.75)],
        4: [
            (s * 0.25, s * 0.25),
            (s * 0.75, s * 0.25),
            (s * 0.25, s * 0.75),
            (s * 0.75, s * 0.75),
        ],
        5: [
            (s * 0.25, s * 0.25),
            (s * 0.75, s * 0.25),
            (s * 0.5, s * 0.5),
            (s * 0.25, s * 0.75),
            (s * 0.75, s * 0.75),
        ],
        6: [
            (s * 0.25, s * 0.25),
            (s * 0.75, s * 0.25),
            (s * 0.25, s * 0.5),
            (s * 0.75, s * 0.5),
            (s * 0.25, s * 0.75),
            (s * 0.75, s * 0.75),
        ],
    }

    if value in pos_map:
        for pos_x_ratio, pos_y_ratio in pos_map[value]:
            pygame.draw.circle(
                surface, COLOR_BLACK, (x + pos_x_ratio, y + pos_y_ratio), dot_radius
            )


def draw_initial_roll(surface, game_state):
    """
    Dibuja la tirada inicial. Si 'surface' es None, no renderiza,
    permitiendo que la lógica se ejecute en modo de prueba.
    """
    if surface is None:
        return  # Modo de prueba

    draw_brick_background(surface)
    draw_decorative_banner(surface)

    title = font_title.render("Tirada Inicial", True, COLOR_TEXT_DARK)
    surface.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 160))

    if game_state["first_roll_data"].get("rolled", False):
        p1_name = game_state["player_names"][PLAYER_WHITE]
        p2_name = game_state["player_names"][PLAYER_BLACK]
        p1_roll = game_state["first_roll_data"][PLAYER_WHITE]
        p2_roll = game_state["first_roll_data"][PLAYER_BLACK]

        # --- Panel Jugador 1 (Izquierda) - Posiciones ajustadas ---
        p1_panel_x = SCREEN_WIDTH / 4 - 100
        p1_text = font_message.render(f"{p1_name} (Blancas)", True, COLOR_TEXT_DARK)
        surface.blit(p1_text, (p1_panel_x + 100 - p1_text.get_width() / 2, 320))
        draw_dice(surface, p1_roll, p1_panel_x + 50, 370, size=100)

        # --- Panel Jugador 2 (Derecha) - Posiciones ajustadas ---
        p2_panel_x = SCREEN_WIDTH * 3 / 4 - 100
        p2_text = font_message.render(f"{p2_name} (Negras)", True, COLOR_TEXT_DARK)
        surface.blit(p2_text, (p2_panel_x + 100 - p2_text.get_width() / 2, 320))
        draw_dice(surface, p2_roll, p2_panel_x + 50, 370, size=100)

        # --- Mensaje del Ganador (posición Y ajustada) ---
        winner = PLAYER_WHITE if p1_roll > p2_roll else PLAYER_BLACK
        winner_name = game_state["player_names"][winner]

        msg_win = f"Gana la tirada: {winner_name}"
        msg_render_win = font_message.render(msg_win, True, COLOR_TEXT_DARK)
        surface.blit(
            msg_render_win, (SCREEN_WIDTH / 2 - msg_render_win.get_width() / 2, 540)
        )

        msg_continue = "Presiona ESPACIO para comenzar"
        msg_render_continue = font_hud_bold.render(msg_continue, True, COLOR_TEXT_DARK)
        surface.blit(
            msg_render_continue,
            (SCREEN_WIDTH / 2 - msg_render_continue.get_width() / 2, 590),
        )


def draw_hud(surface, game_state):
    """Dibuja el nuevo HUD superior y la barra de mensajes central."""
    # --- Barra de Información Superior ---
    hud_rect = pygame.Rect(0, HUD_TOP_MARGIN, SCREEN_WIDTH, HUD_HEIGHT)
    pygame.draw.rect(surface, COLOR_HUD_BG, hud_rect)

    player = game_state["current_player"]
    if player:
        # Turno del jugador (izquierda)
        player_name = game_state["player_names"][player]
        player_color = "Blancas" if player == PLAYER_WHITE else "Negras"
        turn_text = f"Turno: {player_name} - {player_color}"
        turn_render = font_hud.render(turn_text, True, COLOR_HUD_TEXT)
        surface.blit(
            turn_render,
            (
                BOARD_MARGIN_X,
                HUD_TOP_MARGIN + HUD_HEIGHT / 2 - turn_render.get_height() / 2,
            ),
        )

        # Dados y Movimientos (derecha)
        if game_state["dice"]:
            dice_text = f"Dados: {game_state['dice']}"
            moves_text = f"Movimientos: {game_state['moves_remaining']}"
            dice_render = font_hud.render(dice_text, True, COLOR_HUD_TEXT)
            moves_render = font_hud.render(moves_text, True, COLOR_HUD_TEXT)

            # Ancho máximo basado en el texto más largo posible (movimientos de dobles)
            max_text_width = font_hud.size("Movimientos: [6, 6, 6, 6]")[0]

            # Centrado vertical con espaciado
            v_padding = 2
            total_text_height = (
                dice_render.get_height() + moves_render.get_height() + v_padding
            )
            y_start = HUD_TOP_MARGIN + (HUD_HEIGHT - total_text_height) / 2

            # Alineación a la derecha
            x_pos_dice = (
                SCREEN_WIDTH
                - BOARD_MARGIN_X
                - BEAR_OFF_WIDTH
                - BOARD_BEAR_OFF_GAP
                - max_text_width
            )
            x_pos_moves = (
                SCREEN_WIDTH
                - BOARD_MARGIN_X
                - BEAR_OFF_WIDTH
                - BOARD_BEAR_OFF_GAP
                - max_text_width
            )

            surface.blit(dice_render, (x_pos_dice, y_start))
            surface.blit(
                moves_render,
                (x_pos_moves, y_start + dice_render.get_height() + v_padding),
            )

    # --- Barra de Mensajes Central ---
    y_center = BOARD_TOP_Y + BOARD_PLAY_HEIGHT / 2
    msg_rect = pygame.Rect(BOARD_MARGIN_X, y_center - 20, GAME_AREA_WIDTH, 40)
    pygame.draw.rect(surface, (*COLOR_HUD_BG, 200), msg_rect, border_radius=5)

    msg_render = font_hud.render(game_state["message"], True, COLOR_HUD_TEXT)
    surface.blit(
        msg_render,
        (
            msg_rect.centerx - msg_render.get_width() / 2,
            msg_rect.centery - msg_render.get_height() / 2,
        ),
    )


# --- 5. Manejo de Input y Lógica Principal ---------------------------------


def draw_highlights(surface, game_state, legal_moves):
    """
    Dibuja resaltados visuales para el punto de origen seleccionado y todos
    sus posibles destinos legales.
    """
    selected = game_state["selected_point"]
    if not selected:
        return

    # Resaltar el punto de origen (o la barra)
    if selected == "BAR":
        bar_x = BOARD_MARGIN_X + 6 * POINT_WIDTH
        # Dibuja un rectángulo resaltado en la barra
        pygame.draw.rect(
            surface,
            COLOR_HIGHLIGHT,
            (bar_x, BOARD_TOP_Y, BAR_WIDTH, BOARD_PLAY_HEIGHT),
            5,
        )
    else:
        # Dibuja un polígono resaltado en el punto seleccionado
        pygame.draw.polygon(surface, COLOR_HIGHLIGHT, point_positions[selected], 5)

    # Resaltar todos los destinos posibles desde el origen
    if selected in legal_moves:
        for dest in legal_moves[selected]:
            if dest == "OFF":
                off_area_x = SCREEN_WIDTH - BOARD_MARGIN_X - BEAR_OFF_WIDTH
                off_rect = pygame.Rect(off_area_x, 0, BEAR_OFF_WIDTH, SCREEN_HEIGHT)
                pygame.draw.rect(surface, COLOR_HIGHLIGHT, off_rect, 5)
            else:
                pygame.draw.polygon(surface, COLOR_HIGHLIGHT, point_positions[dest], 5)


def is_inside_triangle(pos, triangle_points):
    """
    Comprueba si un punto está dentro de un triángulo usando coordenadas baricéntricas.
    """
    x, y = pos
    p0, p1, p2 = triangle_points

    A = 0.5 * (
        -p1[1] * p2[0]
        + p0[1] * (-p1[0] + p2[0])
        + p0[0] * (p1[1] - p2[1])
        + p1[0] * p2[1]
    )

    s = (
        1
        / (2 * A)
        * (p0[1] * p2[0] - p0[0] * p2[1] + (p2[1] - p0[1]) * x + (p0[0] - p2[0]) * y)
    )
    t = (
        1
        / (2 * A)
        * (p0[0] * p1[1] - p0[1] * p1[0] + (p0[1] - p1[1]) * x + (p1[0] - p0[0]) * y)
    )

    return s > 0 and t > 0 and (1 - s - t) > 0


def get_point_from_mouse(pos):
    """
    Convierte las coordenadas del ratón en un número de punto del tablero (1-24),
    'BAR' para la barra, o 'OFF' para la zona de bear-off.
    Devuelve la zona clickeada o None si no es una zona válida.
    """
    x, y = pos

    # Detección de clic en la zona de bear-off
    off_area_x = SCREEN_WIDTH - BOARD_MARGIN_X - BEAR_OFF_WIDTH
    if x > off_area_x:
        return "OFF"

    # Detección de clic en la barra central
    bar_x_start = BOARD_MARGIN_X + 6 * POINT_WIDTH
    bar_x_end = bar_x_start + BAR_WIDTH
    if bar_x_start < x < bar_x_end:
        return "BAR"

    # Detección de clic en los puntos
    for i in range(1, 25):
        if is_inside_triangle(pos, point_positions[i]):
            return i

    return None


def handle_menu_events(event, game_data):
    """Maneja los eventos en la pantalla del menú principal."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Se comprueba si 'vs_player' existe antes de acceder a él.
        if "vs_player" in game_data.get("buttons", {}) and game_data["buttons"][
            "vs_player"
        ].collidepoint(event.pos):
            game_data["game_phase"] = "NAME_INPUT"
    return game_data


def handle_name_input_events(event, game_data):
    """Maneja los eventos en la pantalla de entrada de nombres."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Comprobar clic en el botón de "Comenzar Partida"
        if "start_game" in game_data.get("buttons", {}) and game_data["buttons"][
            "start_game"
        ].collidepoint(event.pos):
            p1_name = game_data["player_names"][PLAYER_WHITE].strip()
            p2_name = game_data["player_names"][PLAYER_BLACK].strip()
            if 2 <= len(p1_name) <= 10 and 2 <= len(p2_name) <= 10:
                game_data["game_phase"] = "START_ROLL"
                w_roll, b_roll = roll_dice()
                while w_roll == b_roll:
                    w_roll, b_roll = roll_dice()
                game_data["first_roll_data"].update(
                    {PLAYER_WHITE: w_roll, PLAYER_BLACK: b_roll, "rolled": True}
                )
            else:
                game_data["message"] = (
                    "Los nombres deben tener entre 2 y 10 caracteres."
                )

        # Activar una de las cajas de texto
        for player, box in game_data.get("input_boxes", {}).items():
            if box.collidepoint(event.pos):
                game_data["active_input"] = player
                return game_data  # Devolver estado actualizado

    # Manejo de la entrada de teclado
    if event.type == pygame.KEYDOWN and game_data.get("active_input"):
        player = game_data["active_input"]
        current_name = game_data["player_names"].get(player, "")

        if event.key == pygame.K_BACKSPACE:
            game_data["player_names"][player] = current_name[:-1]
        elif len(current_name) < 10:
            # Asegurarse de que el caracter es imprimible y no una tecla de control
            if event.unicode.isprintable():
                game_data["player_names"][player] += event.unicode
    return game_data


def handle_start_roll_events(event, game_data, legal_moves):
    """Maneja los eventos en la pantalla de la tirada inicial."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        w_roll = game_data["first_roll_data"][PLAYER_WHITE]
        b_roll = game_data["first_roll_data"][PLAYER_BLACK]
        winner = PLAYER_WHITE if w_roll > b_roll else PLAYER_BLACK
        winner_name = game_data["player_names"].get(winner, "Jugador")

        game_data.update(
            {
                "current_player": winner,
                "dice": [w_roll, b_roll],
                "moves_remaining": [w_roll, b_roll],
                "game_phase": "PLAY",
                "message": f"Mueven {winner_name}",
            }
        )
        # Limpia y actualiza los movimientos legales para el jugador que empieza
        legal_moves.clear()
        legal_moves.update(
            get_legal_moves(winner, game_data["dice"], game_data)
        )
    return game_data, legal_moves


def check_for_win(game_data):
    """
    Comprueba si algún jugador ha ganado la partida.
    Devuelve el estado del juego actualizado si hay un ganador.
    """
    if game_data["off"][PLAYER_WHITE] == 15:
        game_data.update(
            {
                "message": f"¡Gana {game_data['player_names'][PLAYER_WHITE]}!",
                "game_phase": "GAME_OVER",
            }
        )
    elif game_data["off"][PLAYER_BLACK] == 15:
        game_data.update(
            {
                "message": f"¡Gana {game_data['player_names'][PLAYER_BLACK]}!",
                "game_phase": "GAME_OVER",
            }
        )
    return game_data


def main_loop():
    """
    Bucle principal del juego que maneja eventos y la lógica de turnos.
    """
    global game_data
    clock = pygame.time.Clock()
    running = True
    legal_moves = {}

    while running:
        # --- Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- Lógica de Fases del Juego ---
            phase = game_data["game_phase"]

            # --- Reinicio de la partida (tecla R) ---
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_data = setup_initial_state()
                legal_moves = {}
                print("Partida reiniciada.")
                continue

            # --- Fase: MENÚ ---
            if phase == "MENU":
                game_data = handle_menu_events(event, game_data)

            # --- Fase: ENTRADA DE NOMBRES ---
            elif phase == "NAME_INPUT":
                game_data = handle_name_input_events(event, game_data)

            # --- Fase: TIRADA INICIAL ---
            elif phase == "START_ROLL":
                game_data, legal_moves = handle_start_roll_events(
                    event, game_data, legal_moves
                )

            # --- Fase: JUGANDO ---
            elif phase == "PLAY":
                game_data, legal_moves = handle_play_events(
                    event, game_data, legal_moves
                )

        # --- Dibujado según la Fase ---
        if game_data["game_phase"] == "MENU":
            draw_menu(screen, game_data)
        elif game_data["game_phase"] == "NAME_INPUT":
            draw_name_input(screen, game_data)
        elif game_data["game_phase"] == "START_ROLL":
            draw_initial_roll(screen, game_data)
        elif game_data["game_phase"] in ["PLAY", "GAME_OVER"]:
            draw_board(screen)
            draw_checkers(screen, game_data)
            if game_data["game_phase"] == "PLAY":
                draw_highlights(screen, game_data, legal_moves)
            draw_hud(screen, game_data)

            # Comprobar victoria
            game_data = check_for_win(game_data)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def handle_play_events(event, game_data, legal_moves):
    """Maneja los eventos durante la fase de juego principal."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if not game_data["dice"]:
            d1, d2 = roll_dice()
            game_data["dice"] = [d1, d2]
            if d1 == d2:
                game_data["moves_remaining"] = [d1] * 4
            else:
                game_data["moves_remaining"] = [d1, d2]

            player = game_data["current_player"]
            legal_moves.clear()
            legal_moves.update(
                get_legal_moves(player, game_data["moves_remaining"], game_data)
            )

            if not legal_moves:
                game_data["message"] = "No hay movimientos. Cedes el turno."
                game_data["dice"] = []
                game_data["moves_remaining"] = []
                game_data["current_player"] = get_opponent(player)

    if event.type == pygame.MOUSEBUTTONDOWN:
        player = game_data["current_player"]
        if not player or not game_data["moves_remaining"]:
            return game_data, legal_moves

        clicked_point = get_point_from_mouse(event.pos)

        if game_data["selected_point"] is None:
            if clicked_point in legal_moves:
                game_data["selected_point"] = clicked_point
        else:
            start = game_data["selected_point"]
            end = clicked_point

            if end in legal_moves.get(start, []):
                # Calcular dado usado
                die_used = -1
                if start == "BAR":
                    die_used = (25 - end) if player == "W" else end
                elif end == "OFF":
                    exact_die = start if player == "W" else (25 - start)
                    if exact_die in game_data["moves_remaining"]:
                        die_used = exact_die
                    else:
                        overshoot_dice = [
                            d for d in game_data["moves_remaining"] if d > exact_die
                        ]
                        if overshoot_dice:
                            die_used = min(overshoot_dice)
                else:
                    die_used = abs(end - start)

                # Aplicar movimiento
                game_data = apply_move(start, end, player, game_data)
                game_data["moves_remaining"].remove(die_used)
                game_data["selected_point"] = None

                # Recalcular y cambiar turno si es necesario
                legal_moves.clear()
                legal_moves.update(
                    get_legal_moves(player, game_data["moves_remaining"], game_data)
                )

                if not game_data["moves_remaining"] or not legal_moves:
                    game_data["current_player"] = get_opponent(player)
                    game_data["dice"] = []
                    game_data["moves_remaining"] = []
                    legal_moves.clear()
            else:
                game_data["selected_point"] = None
                game_data["message"] = "Movimiento no válido."
    return game_data, legal_moves


if __name__ == "__main__":
    main_loop()
