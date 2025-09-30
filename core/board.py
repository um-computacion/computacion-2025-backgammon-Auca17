from core.checker import Checker


class Board:
    def __init__(self):
        # points: lista de 24 listas, cada una representa las fichas en cada punto del tablero
        self.__points__ = [[] for _ in range(24)]
        # captured: fichas capturadas (barra), separadas por color
        self.__captured__ = {"white": [], "black": []}
        # home: fichas que ya salieron del tablero (borne off), separadas por color
        self.__home__ = {"white": [], "black": []}
        self._setup_initial_position()

    def _setup_initial_position(self):
        # Inicializa la posición estándar de Backgammon
        self.__points__[0] = [Checker("white") for _ in range(2)]
        self.__points__[11] = [Checker("white") for _ in range(5)]
        self.__points__[16] = [Checker("white") for _ in range(3)]
        self.__points__[18] = [Checker("white") for _ in range(5)]
        self.__points__[23] = [Checker("black") for _ in range(2)]
        self.__points__[12] = [Checker("black") for _ in range(5)]
        self.__points__[7] = [Checker("black") for _ in range(3)]
        self.__points__[5] = [Checker("black") for _ in range(5)]

    def move_checker(self, __color__, __from_point__, __to_point__):
        """
        Mueve una ficha del color dado desde __from_point__ a __to_point__.
        Lanza ValueError si no hay fichas en __from_point__.
        """
        if (
            __from_point__ < 0
            or __from_point__ > 23
            or __to_point__ < 0
            or __to_point__ > 23
        ):
            raise IndexError("Punto fuera de los límites del tablero")
        # Lanzar ValueError si el punto de origen está vacío, sin importar el color
        if not self.__points__[__from_point__]:
            raise ValueError("No checker at from_point")
        if self.__points__[__from_point__][-1].__color__ != __color__:
            raise ValueError("No checker of this color at from_point")
        if (
            self.__points__[__to_point__]
            and self.__points__[__to_point__][-1].__color__ != __color__
            and len(self.__points__[__to_point__]) > 1
        ):
            raise ValueError("Cannot move to a blocked point")
        checker = self.__points__[__from_point__].pop()
        # Captura si hay una ficha rival sola
        if (
            self.__points__[__to_point__]
            and self.__points__[__to_point__][-1].__color__ != __color__
            and len(self.__points__[__to_point__]) == 1
        ):
            captured = self.__points__[__to_point__].pop()
            self.__captured__[captured.__color__].append(captured)
        self.__points__[__to_point__].append(checker)

    def bear_off(self, color, from_point):
        """
        Saca una ficha del color dado desde from_point al home.
        Verifica que haya una ficha del color en from_point.
        """
        if (
            not self.__points__[from_point]
            or self.__points__[from_point][-1].color != color
        ):
            raise ValueError("No checker of this color at from_point")
        checker = self.__points__[from_point].pop()
        self.__home__[color].append(checker)

    def enter_from_captured(self, color, to_point):
        """
        Reingresa una ficha capturada (de la barra) al tablero en to_point.
        Valida que haya fichas capturadas y que el punto de entrada no esté bloqueado.
        Si hay una ficha rival sola, la captura.
        """
        if not self.__captured__[color]:
            raise ValueError("No checker on the bar")
        if (
            self.__points__[to_point]
            and self.__points__[to_point][-1].color != color
            and len(self.__points__[to_point]) > 1
        ):
            raise ValueError("Cannot enter to a blocked point")
        checker = self.__captured__[color].pop()
        # Captura si hay una ficha rival sola
        if (
            self.__points__[to_point]
            and self.__points__[to_point][-1].color != color
            and len(self.__points__[to_point]) == 1
        ):
            captured = self.__points__[to_point].pop()
            self.__captured__[captured.color].append(captured)
        self.__points__[to_point].append(checker)

    def get_point(self, index):
        """
        Devuelve la lista de fichas en el punto index.
        """
        return self.__points__[index]

    def get_captured(self, color):
        """
        Devuelve la lista de fichas capturadas (barra) del color dado.
        """
        return self.__captured__[color]

    def get_home(self, color):
        """
        Devuelve la lista de fichas que ya salieron del tablero (borne off) del color dado.
        """
        return self.__home__[color]

    def get_point_count(self, index):
        """
        Devuelve la cantidad de fichas en el punto dado.
        :param index: Índice del punto (0-23).
        :return: Número de fichas en el punto.
        """
        return len(self.__points__[index])

    @property
    def __points_status__(self):
        """
        Devuelve una lista de diccionarios con la cantidad de fichas en cada punto.
        Esto permite compatibilidad con tests que usan ['count'].
        """
        return [{"count": len(point)} for point in self.__points__]
