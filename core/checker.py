"""
Módulo que define la clase Checker para representar las fichas del juego Backgammon.

Este módulo contiene la implementación de las fichas (checkers) que se mueven
por el tablero durante el juego. Cada ficha tiene un color que identifica
a qué jugador pertenece.

Classes
-------
Checker
    Representa una ficha individual del juego
"""


class Checker:
    """
    Representa una ficha de Backgammon.

    Atributos:
        __color__ (str): El color de la ficha.
        __position__ (int o str): La posición actual de la ficha en el tablero.
        __is_captured__ (bool): Un indicador de si la ficha ha sido capturada.
    """

    def __init__(self, __color__):
        """
        Inicializa una ficha con un color.

        Args:
            __color__ (str): El color de la ficha.
        """
        if __color__ not in ("white", "black"):
            raise ValueError("El color debe ser 'white' o 'black'")
        self.__color__ = __color__
        self.__position__ = None
        self.__is_captured__ = False

    def move_to(self, __new_position__):
        """
        Mueve la ficha a una nueva posición.

        Args:
            __new_position__ (int o str): La nueva posición.
        """
        self.__position__ = __new_position__

    def capture(self):
        """
        Captura la ficha y la envía a la barra.
        """
        self.__is_captured__ = True
        self.__position__ = "bar"

    def __repr__(self):
        """
        Devuelve una representación de la ficha en formato de texto.
        """
        return f"Checker({self.__color__})"
