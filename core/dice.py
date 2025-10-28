"""
Módulo que define la clase Dice para los dados del juego.

Este módulo contiene la implementación de los dados utilizados en Backgammon,
gestionando las tiradas y la detección de dobles.

Classes
-------
Dice
    Representa el par de dados del juego
"""
import random
class Dice:
    """
    Representa un par de dados para el juego de Backgammon.
    """

    def __init__(self):
        self.__value1__ = None
        self.__value2__ = None

    def roll(self):
        """
        Lanza los dos dados y guarda sus valores.
        """
        self.__value1__ = random.randint(1, 6)
        self.__value2__ = random.randint(1, 6)

    def get_values(self):
        """
        Devuelve una tupla con los valores actuales de los dados.
        """
        return (self.__value1__, self.__value2__)

    def is_double(self):
        """
        Verifica si ambos dados tienen el mismo valor.
        """
        return self.__value1__ == self.__value2__
