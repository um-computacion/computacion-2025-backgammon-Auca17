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

    @property
    def __points_status__(self):
        """
        Devuelve una lista de diccionarios con el conteo de fichas en cada punto.
        """
        return [{"count": len(point)} for point in self.__points__]
