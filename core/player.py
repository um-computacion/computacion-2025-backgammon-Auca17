"""
Módulo que define la clase Player para representar a los jugadores.

Este módulo contiene la implementación de los jugadores del Backgammon,
gestionando su nombre, color de fichas y fichas retiradas del tablero.

Classes
-------
Player
    Representa un jugador del juego con sus propiedades y estado
"""


class Player:
    """
    Representa a un jugador de Backgammon.

    Atributos:
        __name__ (str): El nombre del jugador.
        __color__ (str): El color de las fichas del jugador.
        __checkers__ (list): Una lista de las fichas del jugador.
        __bar_checkers__ (int): El número de fichas en la barra.
        __home_checkers__ (int): El número de fichas en el cuadrante de casa.
    """

    def __init__(self, __name__, __color__, __checkers__=None):
        """
        Inicializa un jugador con un nombre, color y una lista opcional de fichas.

        Args:
            __name__ (str): El nombre del jugador.
            __color__ (str): El color de las fichas del jugador.
            __checkers__ (list, opcional): Una lista de las fichas del jugador. Por defecto es None.
        """
        self.__name__ = __name__
        self.__color__ = __color__
        self.__checkers__ = __checkers__ if __checkers__ is not None else []
        self.__bar_checkers__ = 0
        self.__home_checkers__ = 0

    def get_name(self):
        """
        Devuelve el nombre del jugador.
        """
        return self.__name__

    def add_bar_checker(self, __checker__=None):
        """
        Incrementa el número de fichas en la barra.
        """
        if __checker__ is not None:
            self.__checkers__.append(__checker__)
        else:
            if hasattr(self, "__bar_checkers__"):
                self.__bar_checkers__ += 1

    def remove_bar_checker(self):
        """
        Decrementa el número de fichas en la barra.
        """
        if self.__bar_checkers__ > 0:
            self.__bar_checkers__ -= 1

    def add_home_checker(self):
        """
        Incrementa el número de fichas en el cuadrante de casa.
        """
        self.__home_checkers__ += 1

    def get_bar_checkers(self):
        """
        Devuelve el número de fichas en la barra.
        """
        return self.__bar_checkers__

    def get_home_checkers(self):
        """
        Devuelve el número de fichas en el cuadrante de casa.
        """
        return self.__home_checkers__

    def add_checker(self, __checker__):
        """
        Añade una ficha a la lista de fichas del jugador.
        """
        self.__checkers__.append(__checker__)

    def remove_checker(self, __checker__):
        """
        Elimina una ficha de la lista de fichas del jugador si existe.
        """
        if __checker__ in self.__checkers__:
            self.__checkers__.remove(__checker__)

    @property
    def checkers(self):
        """
        Proporciona acceso de solo lectura a la lista de fichas del jugador.
        """
        return self.__checkers__
