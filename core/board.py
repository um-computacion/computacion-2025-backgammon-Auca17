# c:\Users\Rufda\Desktop\Python\computacion-2025-backgammon-Auca17\board.py

from checker import Checker

class Board:
    def __init__(self):
        # points: lista de 24 listas, cada una representa las fichas en cada punto del tablero
        self.points = [[] for _ in range(24)]
        # captured: fichas capturadas (barra), separadas por color
        self.captured = { 'white': [], 'black': [] }
        # home: fichas que ya salieron del tablero (borne off), separadas por color
        self.home = { 'white': [], 'black': [] }
        self._setup_initial_position()

    def _setup_initial_position(self):
        # Inicializa la posición estándar de Backgammon
        self.points[0] = [Checker('white') for _ in range(2)]
        self.points[11] = [Checker('white') for _ in range(5)]
        self.points[16] = [Checker('white') for _ in range(3)]
        self.points[18] = [Checker('white') for _ in range(5)]
        self.points[23] = [Checker('black') for _ in range(2)]
        self.points[12] = [Checker('black') for _ in range(5)]
        self.points[7] = [Checker('black') for _ in range(3)]
        self.points[5] = [Checker('black') for _ in range(5)]

    def move_checker(self, color, from_point, to_point):
        """
        Mueve una ficha del color dado desde from_point a to_point.
        Valida que el movimiento sea legal según las reglas estándar:
        - Debe haber una ficha del color en from_point.
        - to_point debe estar dentro del rango.
        - No puede moverse a un punto bloqueado (más de una ficha rival).
        - Si hay una ficha rival sola en to_point, la captura y la manda a la barra.
        """
        if not self.points[from_point] or self.points[from_point][-1].color != color:
            raise ValueError("No checker of this color at from_point")
        if to_point < 0 or to_point > 23:
            raise ValueError("Invalid destination point")
        if self.points[to_point] and self.points[to_point][-1].color != color and len(self.points[to_point]) > 1:
            raise ValueError("Cannot move to a blocked point")
        checker = self.points[from_point].pop()
        # Captura si hay una ficha rival sola
        if self.points[to_point] and self.points[to_point][-1].color != color and len(self.points[to_point]) == 1:
            captured = self.points[to_point].pop()
            self.captured[captured.color].append(captured)
        self.points[to_point].append(checker)

    def bear_off(self, color, from_point):
        """
        Saca una ficha del color dado desde from_point al home.
        Verifica que haya una ficha del color en from_point.
        """
        if not self.points[from_point] or self.points[from_point][-1].color != color:
            raise ValueError("No checker of this color at from_point")
        checker = self.points[from_point].pop()
        self.home[color].append(checker)

    def enter_from_captured(self, color, to_point):
        """
        Reingresa una ficha capturada (de la barra) al tablero en to_point.
        Valida que haya fichas capturadas y que el punto de entrada no esté bloqueado.
        Si hay una ficha rival sola, la captura.
        """
        if not self.captured[color]:
            raise ValueError("No checker on the bar")
        if self.points[to_point] and self.points[to_point][-1].color != color and len(self.points[to_point]) > 1:
            raise ValueError("Cannot enter to a blocked point")
        checker = self.captured[color].pop()
        # Captura si hay una ficha rival sola
        if self.points[to_point] and self.points[to_point][-1].color != color and len(self.points[to_point]) == 1:
            captured = self.points[to_point].pop()
            self.captured[captured.color].append(captured)
        self.points[to_point].append(checker)

    def get_point(self, index):
        """
        Devuelve la lista de fichas en el punto index.
        """
        return self.points[index]

    def get_captured(self, color):
        """
        Devuelve la lista de fichas capturadas (barra) del color dado.
        """
        return self.captured[color]

    def get_home(self, color):
        """
        Devuelve la lista de fichas que ya salieron del tablero (borne off) del color dado.
        """
        return self.home[color]