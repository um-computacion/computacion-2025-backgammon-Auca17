"""
Módulo que define el tablero del juego Backgammon.

Este módulo contiene la clase Board que representa el tablero de juego,
gestionando las posiciones de las fichas, la barra y las fichas retiradas.
Implementa la configuración inicial estándar del Backgammon.

Classes
-------
Board
    Representa el tablero de juego con sus 24 puntos y zonas especiales
"""

from core.checker import Checker

class Board:
    """
    Representa el tablero de Backgammon.

    Atributos:
        __points__ (list): Una lista de 24 listas, donde cada una representa un punto en el tablero.
        __captured__ (dict): Un diccionario que almacena las fichas capturadas de cada color.
        __home__ (dict): Un diccionario que almacena las fichas que han salido del tablero para cada color.
    """

    def __init__(self):
        """
        Inicializa el tablero con la posición de inicio estándar.
        """
        self.__points__ = [[] for _ in range(24)]
        self.__captured__ = {"white": [], "black": []}
        self.__home__ = {"white": [], "black": []}
        self.__setup_initial_position__()

    def __setup_initial_position__(self):
        """
        Configura la posición inicial de las fichas en el tablero.
        """
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
        Mueve una ficha de un punto a otro.

        Args:
            __color__ (str): El color de la ficha a mover.
            __from_point__ (int): El punto de partida.
            __to_point__ (int): El punto de destino.
        """
        if not (0 <= __from_point__ < 24 and 0 <= __to_point__ < 24):
            raise IndexError("El punto está fuera de los límites del tablero")
        if not self.__points__[__from_point__]:
            raise ValueError("No hay ficha en el punto de origen")
        if self.__points__[__from_point__][-1].__color__ != __color__:
            raise ValueError("No hay ficha de este color en el punto de origen")
        if (
            len(self.__points__[__to_point__]) > 1
            and self.__points__[__to_point__][-1].__color__ != __color__
        ):
            raise ValueError("No se puede mover a un punto bloqueado")

        checker = self.__points__[__from_point__].pop()

        if (
            len(self.__points__[__to_point__]) == 1
            and self.__points__[__to_point__][-1].__color__ != __color__
        ):
            captured = self.__points__[__to_point__].pop()
            self.__captured__[captured.__color__].append(captured)

        self.__points__[__to_point__].append(checker)

    def bear_off(self, __color__, __from_point__):
        """
        Saca una ficha del tablero.

        Args:
            __color__ (str): El color de la ficha a sacar.
            __from_point__ (int): El punto desde el cual se saca la ficha.
        """
        if (
            not self.__points__[__from_point__]
            or self.__points__[__from_point__][-1].__color__ != __color__
        ):
            raise ValueError("No hay una ficha de este color en el punto de origen")
        checker = self.__points__[__from_point__].pop()
        self.__home__[__color__].append(checker)

    def enter_from_captured(self, __color__, __to_point__):
        """
        Reingresa una ficha capturada al tablero.

        Args:
            __color__ (str): El color de la ficha a reingresar.
            __to_point__ (int): El punto al que se reingresa la ficha.
        """
        if not self.__captured__[__color__]:
            raise ValueError("No hay fichas en la barra")
        if (
            len(self.__points__[__to_point__]) > 1
            and self.__points__[__to_point__][-1].__color__ != __color__
        ):
            raise ValueError("No se puede ingresar a un punto bloqueado")

        checker = self.__captured__[__color__].pop()

        if (
            len(self.__points__[__to_point__]) == 1
            and self.__points__[__to_point__][-1].__color__ != __color__
        ):
            captured = self.__points__[__to_point__].pop()
            self.__captured__[captured.__color__].append(captured)

        self.__points__[__to_point__].append(checker)

    def get_point(self, __index__):
        """
        Devuelve la lista de fichas en un punto dado.

        Args:
            __index__ (int): El índice del punto.

        Returns:
            list: La lista de fichas en el punto.
        """
        return self.__points__[__index__]

    def get_captured(self, __color__):
        """
        Devuelve la lista de fichas capturadas de un color dado.

        Args:
            __color__ (str): El color de las fichas.

        Returns:
            list: La lista de fichas capturadas.
        """
        return self.__captured__[__color__]

    def get_home(self, __color__):
        """
        Devuelve la lista de fichas que han salido del tablero de un color dado.

        Args:
            __color__ (str): El color de las fichas.

        Returns:
            list: La lista de fichas que han salido.
        """
        return self.__home__[__color__]

    def get_point_count(self, __index__):
        """
        Devuelve el número de fichas en un punto dado.

        Args:
            __index__ (int): El índice del punto.

        Returns:
            int: El número de fichas en el punto.
        """
        return len(self.__points__[__index__])

    def get_2d_representation(self):
        """
        Genera una representación en cadena de texto en 2D del tablero de Backgammon.
        La representación muestra los puntos, las fichas ('O' para blancas, 'X' para negras),
        la barra para fichas capturadas, y el contador de fichas fuera del tablero.
        """

        def _get_point_string(point, row):
            """Devuelve la representación de 3 caracteres para una fila en un punto."""
            # Fila virtual para contadores de fichas > 5
            if row == 5:
                if len(point) > 5:
                    return f"x{len(point)}".ljust(3)
                return "   "
            # Filas de fichas visibles
            if len(point) > row:
                checker = "O" if point[row].__color__ == "white" else "X"
                return f" {checker} "
            return "   "

        # Encabezados de números de puntos
        top_header = " ".join([f"{i:>2}" for i in range(12, 6, -1)])
        bottom_header = " ".join([f"{i:>2}" for i in range(13, 19)])
        top_footer = " ".join([f"{i:>2}" for i in range(6, 0, -1)])
        bottom_footer = " ".join([f"{i:>2}" for i in range(19, 25)])

        board_str = f"\n{top_header} | BAR | {top_footer}\n"
        board_str += "+--------------------+-----+--------------------+\n"

        # Filas de la mitad superior (incluyendo contadores)
        for i in range(6):  # 0-4 para fichas, 5 para contadores
            line = ""
            for p in range(11, 5, -1):
                line += _get_point_string(self.__points__[p], i)
            line += "|     |"
            for p in range(5, -1, -1):
                line += _get_point_string(self.__points__[p], i)
            board_str += line + "\n"

        # Barra central con conteo de fichas capturadas
        white_captured = len(self.__captured__["white"])
        black_captured = len(self.__captured__["black"])
        bar_display = f"W:{white_captured} B:{black_captured}"
        board_str += (
            f"                     |{bar_display.center(5)}|                     \n"
        )

        # Filas de la mitad inferior (incluyendo contadores)
        for i in range(5, -1, -1):  # 5 para contadores, 4-0 para fichas
            line = ""
            for p in range(12, 18):
                line += _get_point_string(self.__points__[p], i)
            line += "|     |"
            for p in range(18, 24):
                line += _get_point_string(self.__points__[p], i)
            board_str += line + "\n"

        # Pie de página
        board_str += "+--------------------+-----+--------------------+\n"
        board_str += f"{bottom_header} |     | {bottom_footer}\n"

        # Conteo de fichas en casa
        white_home = len(self.__home__["white"])
        black_home = len(self.__home__["black"])
        board_str += f"\nFichas en casa - Blancas: {white_home}, Negras: {black_home}\n"

        return board_str

    @property
    def __points_status__(self):
        """
        Devuelve una lista de diccionarios con el conteo de fichas en cada punto.
        """
        return [{"count": len(point)} for point in self.__points__]
