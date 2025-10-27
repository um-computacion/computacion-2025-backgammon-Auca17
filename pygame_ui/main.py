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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Backgammon")

# Colores (RGB)
COLOR_BOARD = (210, 180, 140)  # Un color madera claro para el tablero
COLOR_POINT_A = (128, 0, 0)     # Triángulos de color vino
COLOR_POINT_B = (0, 0, 0)         # Triángulos negros
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (20, 20, 20)
COLOR_HIGHLIGHT = (255, 255, 0, 100)  # Amarillo semitransparente para resaltar
COLOR_HUD_BG = (100, 100, 100)
COLOR_HUD_TEXT = (240, 240, 240)

# Fuentes
font_hud = pygame.font.SysFont("Arial", 24)
font_message = pygame.font.SysFont("Arial", 28, bold=True)
font_point_num = pygame.font.SysFont("Arial", 16)

# Geometría del tablero
BOARD_MARGIN = 30
BAR_WIDTH = 60
POINT_WIDTH = (SCREEN_WIDTH - 2 * BOARD_MARGIN - BAR_WIDTH) / 12
POINT_HEIGHT = SCREEN_HEIGHT * 0.4

# Posiciones de los puntos (triángulos)
# Los puntos se numeran del 1 al 24. El movimiento de las blancas es 24 -> 1,
# y el de las negras es 1 -> 24.
point_positions = {}
for i in range(12):
    # Puntos de abajo (1 a 12)
    x_base = BOARD_MARGIN + i * POINT_WIDTH
    if i >= 6:
        x_base += BAR_WIDTH  # Salto de la barra
    point_positions[12 - i] = [(x_base, SCREEN_HEIGHT - BOARD_MARGIN),
                               (x_base + POINT_WIDTH, SCREEN_HEIGHT - BOARD_MARGIN),
                               (x_base + POINT_WIDTH / 2, SCREEN_HEIGHT - BOARD_MARGIN - POINT_HEIGHT)]
    # Puntos de arriba (24 a 13)
    point_positions[13 + i] = [(x_base, BOARD_MARGIN),
                               (x_base + POINT_WIDTH, BOARD_MARGIN),
                               (x_base + POINT_WIDTH / 2, BOARD_MARGIN + POINT_HEIGHT)]

# --- 2. Modelo de Datos (Estado del Juego) ---------------------------------

# Identificadores para los jugadores
PLAYER_WHITE = 'W'
PLAYER_BLACK = 'B'

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
    board[0] = [PLAYER_BLACK] * 2    # Punto 1
    board[5] = [PLAYER_WHITE] * 5    # Punto 6
    board[7] = [PLAYER_WHITE] * 3    # Punto 8
    board[11] = [PLAYER_BLACK] * 5   # Punto 12
    board[12] = [PLAYER_WHITE] * 5   # Punto 13
    board[16] = [PLAYER_BLACK] * 3   # Punto 17
    board[18] = [PLAYER_BLACK] * 5   # Punto 19
    board[23] = [PLAYER_WHITE] * 2   # Punto 24

    # Fichas en la barra (inicialmente vacía para ambos jugadores)
    bar = {PLAYER_WHITE: 0, PLAYER_BLACK: 0}

    # Fichas retiradas (bear-off, inicialmente cero para ambos)
    off = {PLAYER_WHITE: 0, PLAYER_BLACK: 0}

    # Diccionario principal que encapsula todo el estado del juego
    game_state = {
        'board': board,
        'bar': bar,
        'off': off,
        'current_player': None,       # Se decide con la primera tirada
        'dice': [],                   # ej: [4, 5]
        'moves_remaining': [],        # Movimientos disponibles según los dados
        'selected_point': None,       # Punto de origen seleccionado
        'message': "Tiren para ver quién empieza.",
        'game_phase': 'START_ROLL',   # Fases: START_ROLL, PLAY, GAME_OVER
        'first_roll_data': {PLAYER_WHITE: 0, PLAYER_BLACK: 0, 'rolled': False},
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
    board = game_state['board']
    if game_state['bar'][player] > 0:
        return False  # No se puede hacer bear-off con fichas en la barra.

    home_board_indices = range(0, 6) if player == PLAYER_WHITE else range(18, 24)
    checkers_in_home = 0
    
    for i in home_board_indices:
        if board[i] and board[i][0] == player:
            checkers_in_home += len(board[i])

    # El total de fichas en casa más las retiradas debe ser 15.
    return checkers_in_home + game_state['off'][player] == 15

def get_legal_moves(player, dice, game_state):
    """
    Encuentra todos los movimientos legales para un jugador dados los resultados de los dados.
    Devuelve un diccionario donde las claves son los puntos de origen y los valores
    son listas de posibles puntos de destino.
    """
    legal_moves = {}
    board = game_state['board']
    
    # --- Regla 1: Reingreso desde la barra ---
    if game_state['bar'][player] > 0:
        for die in set(dice):
            # El destino se calcula desde un "punto 0" o "punto 25" conceptual.
            if player == PLAYER_WHITE:
                target_point_idx = 24 - die
            else: # PLAYER_BLACK
                target_point_idx = die - 1
            
            # Comprobar si el punto de entrada está bloqueado
            if len(board[target_point_idx]) <= 1 or board[target_point_idx][0] == player:
                if 'BAR' not in legal_moves:
                    legal_moves['BAR'] = []
                legal_moves['BAR'].append(target_point_idx + 1)
        return legal_moves # Si hay fichas en la barra, no se pueden hacer otros movimientos

    # --- Regla 2: Movimientos normales y Bear-off ---
    can_do_bear_off = can_bear_off(player, game_state)

    for point_idx, checkers in enumerate(board):
        if checkers and checkers[0] == player:
            start_point = point_idx + 1
            
            for die in set(dice):
                if player == PLAYER_WHITE:
                    target_point_idx = point_idx - die
                else: # PLAYER_BLACK
                    target_point_idx = point_idx + die

                # Movimiento normal dentro del tablero
                if 0 <= target_point_idx < 24:
                    if len(board[target_point_idx]) <= 1 or board[target_point_idx][0] == player:
                        if start_point not in legal_moves:
                            legal_moves[start_point] = []
                        legal_moves[start_point].append(target_point_idx + 1)
                
                # Bear-off
                elif can_do_bear_off:
                    if player == PLAYER_WHITE and target_point_idx < 0:
                        # Regla exacta: la ficha está en el punto que marca el dado
                        if start_point == die:
                            if start_point not in legal_moves: legal_moves[start_point] = []
                            legal_moves[start_point].append('OFF')
                        # Regla de excedente
                        else:
                            # Regla de excedente: solo se puede usar un dado mayor si no hay
                            # fichas en puntos más altos.
                            is_further_checker = False
                            for p in range(start_point + 1, 7): # Para blancas, puntos más altos son 6, 5, 4...
                                if board[p - 1] and board[p - 1][0] == player:
                                    is_further_checker = True
                                    break
                            if not is_further_checker and die > start_point:
                                if start_point not in legal_moves: legal_moves[start_point] = []
                                legal_moves[start_point].append('OFF')
                                
                    elif player == PLAYER_BLACK and target_point_idx >= 24:
                        # Regla exacta
                        if (25 - start_point) == die:
                            if start_point not in legal_moves: legal_moves[start_point] = []
                            legal_moves[start_point].append('OFF')
                        # Regla de excedente
                        else:
                            is_further_checker = False
                            for p in range(start_point - 1, 18, -1): # Para negras, puntos más altos son 19, 20...
                                if board[p - 1] and board[p - 1][0] == player:
                                    is_further_checker = True
                                    break
                            if not is_further_checker and die > (25 - start_point):
                                if start_point not in legal_moves: legal_moves[start_point] = []
                                legal_moves[start_point].append('OFF')
    return legal_moves

def apply_move(start_point, end_point, player, game_state):
    """
    Aplica un movimiento al estado del juego.
    start_point puede ser un número (1-24) o 'BAR'.
    end_point puede ser un número (1-24) o 'OFF'.
    """
    board = game_state['board']
    opponent = get_opponent(player)
    
    # 1. Quitar ficha del origen
    if start_point == 'BAR':
        game_state['bar'][player] -= 1
    else:
        board[start_point - 1].pop()

    # 2. Añadir ficha al destino
    if end_point == 'OFF':
        game_state['off'][player] += 1
    else:
        target_idx = end_point - 1
        # Comprobar si se come una ficha rival (blot)
        if board[target_idx] and board[target_idx][0] == opponent:
            board[target_idx].pop()
            game_state['bar'][opponent] += 1
            game_state['message'] = f"{'Negras' if opponent == 'B' else 'Blancas'} a la barra!"
        board[target_idx].append(player)

    return game_state


# --- 4. Funciones de Dibujo (Renderizado) ----------------------------------

def draw_board(surface):
    """
    Dibuja el tablero de Backgammon, incluyendo los puntos (triángulos) y la barra.
    """
    surface.fill(COLOR_BOARD)

    # Dibuja los 24 puntos (triángulos)
    for i in range(1, 25):
        color = COLOR_POINT_A if (i % 2) != 0 else COLOR_POINT_B
        if 1 <= i <= 6 or 13 <= i <= 18:
             color = COLOR_POINT_B if (i % 2) != 0 else COLOR_POINT_A
        pygame.draw.polygon(surface, color, point_positions[i])

    # Dibuja la barra central
    bar_x = BOARD_MARGIN + 6 * POINT_WIDTH
    pygame.draw.rect(surface, COLOR_HUD_BG, (bar_x, BOARD_MARGIN, BAR_WIDTH, SCREEN_HEIGHT - 2 * BOARD_MARGIN))
    
    # Dibuja los números de los puntos
    for i in range(1, 25):
        text = font_point_num.render(str(i), True, COLOR_HUD_TEXT)
        x_pos = point_positions[i][2][0] - text.get_width() / 2
        y_pos = BOARD_MARGIN + POINT_HEIGHT + 10 if i > 12 else SCREEN_HEIGHT - BOARD_MARGIN - POINT_HEIGHT - 30
        surface.blit(text, (x_pos, y_pos))


def draw_checkers(surface, game_state):
    """
    Dibuja las fichas en el tablero, la barra y la zona de bear-off.
    """
    board = game_state['board']
    bar = game_state['bar']
    off = game_state['off']
    checker_radius = int(POINT_WIDTH * 0.4)

    # Dibuja las fichas en los puntos
    for point_idx, checkers in enumerate(board):
        point_num = point_idx + 1
        x_center = point_positions[point_num][2][0]
        
        for i, checker_color in enumerate(checkers):
            color = COLOR_WHITE if checker_color == PLAYER_WHITE else COLOR_BLACK
            
            if point_num <= 12: # Puntos de abajo
                y_pos = SCREEN_HEIGHT - BOARD_MARGIN - checker_radius - (i * 2 * checker_radius)
            else: # Puntos de arriba
                y_pos = BOARD_MARGIN + checker_radius + (i * 2 * checker_radius)
            
            # Si hay más de 5 fichas, se muestra un contador
            if i >= 4 and len(checkers) > 5:
                y_pos_last = SCREEN_HEIGHT - BOARD_MARGIN - checker_radius - (4 * 2 * checker_radius) if point_num <= 12 else BOARD_MARGIN + checker_radius + (4 * 2 * checker_radius)
                pygame.draw.circle(surface, color, (x_center, y_pos_last), checker_radius)
                pygame.draw.circle(surface, (0,0,0) if color == COLOR_WHITE else (255,255,255), (x_center, y_pos_last), checker_radius, 2)
                
                count_text = font_hud.render(f"x{len(checkers)}", True, COLOR_HIGHLIGHT)
                surface.blit(count_text, (x_center - count_text.get_width()/2, y_pos_last - count_text.get_height()/2))
                break 
            
            pygame.draw.circle(surface, color, (x_center, y_pos), checker_radius)
            pygame.draw.circle(surface, (0,0,0) if color == COLOR_WHITE else (255,255,255), (x_center, y_pos), checker_radius, 2)

    # Dibuja las fichas en la barra
    bar_x = BOARD_MARGIN + 6 * POINT_WIDTH + BAR_WIDTH / 2
    for i in range(bar[PLAYER_WHITE]):
        y_pos = SCREEN_HEIGHT / 2 + 100 + i * (2 * checker_radius)
        pygame.draw.circle(surface, COLOR_WHITE, (bar_x, y_pos), checker_radius)
        pygame.draw.circle(surface, COLOR_BLACK, (bar_x, y_pos), checker_radius, 2)
    for i in range(bar[PLAYER_BLACK]):
        y_pos = SCREEN_HEIGHT / 2 - 100 - i * (2 * checker_radius)
        pygame.draw.circle(surface, COLOR_BLACK, (bar_x, y_pos), checker_radius)
        pygame.draw.circle(surface, COLOR_WHITE, (bar_x, y_pos), checker_radius, 2)

    # Dibuja las fichas retiradas (off)
    off_x = SCREEN_WIDTH - BOARD_MARGIN + checker_radius / 2
    for i in range(off[PLAYER_WHITE]):
        y_pos = SCREEN_HEIGHT - BOARD_MARGIN - checker_radius - i * int(checker_radius * 1.5)
        pygame.draw.circle(surface, COLOR_WHITE, (off_x, y_pos), checker_radius, 5)
    for i in range(off[PLAYER_BLACK]):
        y_pos = BOARD_MARGIN + checker_radius + i * int(checker_radius * 1.5)
        pygame.draw.circle(surface, COLOR_BLACK, (off_x, y_pos), checker_radius, 5)


def draw_hud(surface, game_state):
    """
    Dibuja el panel de información (HUD) con el estado actual del juego.
    """
    player = game_state['current_player']
    dice = game_state['dice']
    moves = game_state['moves_remaining']
    message = game_state['message']

    hud_rect = pygame.Rect(0, SCREEN_HEIGHT / 2 - 50, SCREEN_WIDTH, 100)
    pygame.draw.rect(surface, COLOR_HUD_BG, hud_rect)
    
    # Mensaje central
    msg_render = font_message.render(message, True, COLOR_HUD_TEXT)
    surface.blit(msg_render, (SCREEN_WIDTH/2 - msg_render.get_width()/2, hud_rect.centery - msg_render.get_height()/2))

    # Turno del jugador
    if player:
        player_text = f"Turno: {'Blancas' if player == PLAYER_WHITE else 'Negras'}"
        player_render = font_hud.render(player_text, True, COLOR_HUD_TEXT)
        surface.blit(player_render, (BOARD_MARGIN, hud_rect.y + 10))

    # Dados
    if dice:
        dice_text = f"Dados: {dice}"
        dice_render = font_hud.render(dice_text, True, COLOR_HUD_TEXT)
        surface.blit(dice_render, (BOARD_MARGIN, hud_rect.y + 40))
        
    # Movimientos restantes
    if moves:
        moves_text = f"Movimientos: {moves}"
        moves_render = font_hud.render(moves_text, True, COLOR_HUD_TEXT)
        surface.blit(moves_render, (BOARD_MARGIN, hud_rect.y + 70))


# --- 5. Manejo de Input y Lógica Principal ---------------------------------

def draw_highlights(surface, game_state, legal_moves):
    """
    Dibuja resaltados visuales para el punto de origen seleccionado y todos
    sus posibles destinos legales.
    """
    selected = game_state['selected_point']
    if not selected:
        return

    # Resaltar el punto de origen (o la barra)
    if selected == 'BAR':
        bar_x = BOARD_MARGIN + 6 * POINT_WIDTH
        # Dibuja un rectángulo resaltado en la barra
        pygame.draw.rect(surface, COLOR_HIGHLIGHT, (bar_x, BOARD_MARGIN, BAR_WIDTH, SCREEN_HEIGHT - 2 * BOARD_MARGIN), 5)
    else:
        # Dibuja un polígono resaltado en el punto seleccionado
        pygame.draw.polygon(surface, COLOR_HIGHLIGHT, point_positions[selected], 5)

    # Resaltar todos los destinos posibles desde el origen
    if selected in legal_moves:
        for dest in legal_moves[selected]:
            if dest == 'OFF':
                # Aquí se podría añadir un resaltado para la zona de bear-off
                off_rect_w = pygame.Rect(SCREEN_WIDTH - BOARD_MARGIN - 50, BOARD_MARGIN, 50, SCREEN_HEIGHT/2 - BOARD_MARGIN)
                off_rect_b = pygame.Rect(SCREEN_WIDTH - BOARD_MARGIN - 50, SCREEN_HEIGHT/2, 50, SCREEN_HEIGHT/2 - BOARD_MARGIN)
                pygame.draw.rect(surface, COLOR_HIGHLIGHT, off_rect_w if game_state['current_player'] == PLAYER_WHITE else off_rect_b, 5)
            else:
                 pygame.draw.polygon(surface, COLOR_HIGHLIGHT, point_positions[dest], 5)

def get_point_from_mouse(pos):
    """
    Convierte las coordenadas del ratón en un número de punto del tablero (1-24).
    Devuelve el número del punto o None si no se hizo clic en un punto válido.
    """
    x, y = pos
    
    # Clic en la barra
    bar_x_start = BOARD_MARGIN + 6 * POINT_WIDTH
    bar_x_end = bar_x_start + BAR_WIDTH
    if bar_x_start < x < bar_x_end:
        return 'BAR'

    # Clic en los puntos superiores (13-24)
    for i in range(13, 25):
        x_base = point_positions[i][0][0]
        rect = pygame.Rect(x_base, BOARD_MARGIN, POINT_WIDTH, POINT_HEIGHT)
        if rect.collidepoint(x, y):
            return i

    # Clic en los puntos inferiores (1-12)
    for i in range(1, 13):
        x_base = point_positions[i][0][0]
        rect = pygame.Rect(x_base, SCREEN_HEIGHT - BOARD_MARGIN - POINT_HEIGHT, POINT_WIDTH, POINT_HEIGHT)
        if rect.collidepoint(x, y):
            return i
            
    return None

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

            # --- Reinicio de la partida ---
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_data = setup_initial_state()
                legal_moves = {}
                print("Partida reiniciada.")
                continue

            # --- Tirada de Dados (Barra Espaciadora) ---
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Tirada inicial para decidir quién empieza
                if game_data['game_phase'] == 'START_ROLL' and not game_data['first_roll_data']['rolled']:
                    w_roll, b_roll = roll_dice()
                    while w_roll == b_roll: # Re-roll en caso de empate
                         w_roll, b_roll = roll_dice()
                    
                    game_data['first_roll_data'][PLAYER_WHITE] = w_roll
                    game_data['first_roll_data'][PLAYER_BLACK] = b_roll
                    game_data['first_roll_data']['rolled'] = True
                    
                    winner = PLAYER_WHITE if w_roll > b_roll else PLAYER_BLACK
                    game_data['current_player'] = winner
                    game_data['dice'] = [w_roll, b_roll]
                    game_data['moves_remaining'] = list(game_data['dice'])
                    game_data['game_phase'] = 'PLAY'
                    game_data['message'] = f"Ganan {'Blancas' if winner == 'W' else 'Negras'}. Mueven {w_roll}-{b_roll}"
                    legal_moves = get_legal_moves(winner, game_data['dice'], game_data)

                # Tirada normal al inicio de un turno
                elif game_data['game_phase'] == 'PLAY' and not game_data['dice']:
                    d1, d2 = roll_dice()
                    game_data['dice'] = [d1, d2]
                    if d1 == d2: # Dobles
                        game_data['moves_remaining'] = [d1] * 4
                    else:
                        game_data['moves_remaining'] = [d1, d2]
                    
                    player = game_data['current_player']
                    game_data['message'] = f"Turno de {'Blancas' if player == 'W' else 'Negras'}"
                    legal_moves = get_legal_moves(player, game_data['moves_remaining'], game_data)

                    # Si no hay movimientos legales, se cede el turno
                    if not legal_moves:
                        game_data['message'] = "No hay movimientos. Cedes el turno."
                        # Se podría añadir un delay aquí
                        game_data['dice'] = []
                        game_data['moves_remaining'] = []
                        game_data['current_player'] = get_opponent(player)


            # --- Manejo de Clics del Ratón ---
            if event.type == pygame.MOUSEBUTTONDOWN and game_data['game_phase'] == 'PLAY':
                player = game_data['current_player']
                if not player or not game_data['moves_remaining']:
                    continue

                clicked_point = get_point_from_mouse(event.pos)
                
                # 1. Seleccionar origen
                if game_data['selected_point'] is None:
                    if clicked_point in legal_moves:
                        game_data['selected_point'] = clicked_point
                        # Aquí se podría añadir lógica para resaltar destinos
                
                # 2. Seleccionar destino y mover
                else:
                    start = game_data['selected_point']
                    end = clicked_point
                    
                    if end in legal_moves.get(start, []):
                        # Calcular qué dado se usó
                        die_used = -1
                        if start == 'BAR':
                            die_used = (25 - end) if player == PLAYER_WHITE else end
                        elif end == 'OFF':
                            exact_die = start if player == PLAYER_WHITE else (25 - start)
                            if exact_die in game_data['moves_remaining']:
                                die_used = exact_die
                            else: # Regla de excedente
                                die_used = max(d for d in game_data['moves_remaining'] if d > exact_die)
                        else:
                            die_used = abs(end - start)

                        # Aplicar movimiento
                        game_data = apply_move(start, end, player, game_data)
                        
                        # Actualizar estado
                        game_data['moves_remaining'].remove(die_used)
                        game_data['selected_point'] = None
                        
                        # Recalcular movimientos y comprobar si el turno debe terminar
                        legal_moves = get_legal_moves(player, game_data['moves_remaining'], game_data)
                        
                        if not game_data['moves_remaining'] or not legal_moves:
                            game_data['current_player'] = get_opponent(player)
                            game_data['dice'] = []
                            game_data['moves_remaining'] = []
                            game_data['message'] = f"Turno de {'Blancas' if get_opponent(player) == 'W' else 'Negras'}"
                            legal_moves = {}

                    else: # Clic inválido
                        game_data['selected_point'] = None
                        game_data['message'] = "Movimiento no válido."


        # --- Comprobar Victoria ---
        if game_data['off'][PLAYER_WHITE] == 15:
            game_data['message'] = "¡Ganan las Blancas!"
            game_data['game_phase'] = 'GAME_OVER'
        elif game_data['off'][PLAYER_BLACK] == 15:
            game_data['message'] = "¡Ganan las Negras!"
            game_data['game_phase'] = 'GAME_OVER'

        # --- Lógica de Dibujo ---
        draw_board(screen)
        draw_checkers(screen, game_data)
        if game_data['game_phase'] == 'PLAY':
             draw_highlights(screen, game_data, legal_moves)
        draw_hud(screen, game_data)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_loop()
