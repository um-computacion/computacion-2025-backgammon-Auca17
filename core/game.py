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