from core.board import Board
from core.player import Player

class Game:
    """
    Clase principal que gestiona el flujo del juego de Backgammon.
    Conecta el tablero, los jugadores y controla la partida.
    """

    def __init__(self, player1, player2):
        """
        Inicializa el juego con dos jugadores y un tablero.

        Args:
            player1 (Player): Primer jugador.
            player2 (Player): Segundo jugador.
        """
        self.__board__ = Board()
        self.__players__ = [player1, player2]
        self.__current_turn__ = 0  # Índice del jugador actual
        self.__history__ = []      # Historial de movimientos
        self.__winner__ = None    # Ganador de la partida

    def start(self):
        """
        Inicia la partida y establece el primer turno.
        """
        # Aquí podrías inicializar posiciones, lanzar dados, etc.
        pass

    def switch_turn(self):
        """
        Cambia el turno al siguiente jugador.
        """
        self.__current_turn__ = 1 - self.__current_turn__

    def move(self, from_pos, to_pos):
        """
        Realiza un movimiento si es válido y actualiza el historial.

        Args:
            from_pos (int): Posición de origen.
            to_pos (int): Posición de destino.
        """
        # Validar movimiento, actualizar tablero y fichas
        pass

    def check_winner(self):
        """
        Verifica si algún jugador ha ganado la partida.
        """
        pass

    def reset(self):
        """
        Reinicia el juego para una nueva partida.
        """
        pass

    def get_current_player(self):
        return self.__players__[self.__current_turn__]

    def is_over(self):
        return self.__winner__ is not None

    def get_winner(self):
        return self.__winner__

    def display_board(self):
        print("Board: " + " ".join(str(x) for x in self.__board__))

    def make_move(self, player, from_pos, to_pos):
        if not (0 <= from_pos < 24 and 0 <= to_pos < 24):
            return False
        if player == self.__players__[0] and self.__board__[from_pos] <= 0:
            return False
        if player == self.__players__[1] and self.__board__[from_pos] >= 0:
            return False
        if abs(to_pos - from_pos) != 1:  # Simplified: only adjacent moves
            return False
        if player == self.__players__[0] and self.__board__[to_pos] < 0:
            return False  # Can't land on opponent's checker
        if player == self.__players__[1] and self.__board__[to_pos] > 0:
            return False
        # Move
        self.__board__[from_pos] -= 1 if player == self.__players__[0] else -1
        self.__board__[to_pos] += 1 if player == self.__players__[0] else -1
        # Check win condition (simplified: all checkers off board)
        if all(x >= 0 for x in self.__board__) and self.__players__[0].checkers_off == 2:
            self.__winner__ = self.__players__[0]
        elif all(x <= 0 for x in self.__board__) and self.__players__[1].checkers_off == 2:
            self.__winner__ = self.__players__[1]
        self.__current_turn__ = 1 - self.__current_turn__
        return True