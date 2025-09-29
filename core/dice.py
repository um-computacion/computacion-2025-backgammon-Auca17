import random

class Dice:
    def __init__(self):
        self.__value1__ = None
        self.__value2__ = None

    def roll(self):
        """
        Lanza los dos dados y guarda sus valores.
        Se utiliza en el juego para determinar los movimientos posibles de un jugador.
        """
        self.__value1__ = random.randint(1, 6)
        self.__value2__ = random.randint(1, 6)

    def get_values(self):
        """
        Devuelve una tupla con los valores actuales de los dados.
        Es útil para que otras clases (como Game o Player) consulten los resultados del lanzamiento.
        """
        return (self.__value1__, self.__value2__)

    def is_double(self):
        """
        Verifica si ambos dados tienen el mismo valor.
        Esto es importante en Backgammon, ya que los dobles permiten movimientos adicionales.
        """
        return self.__value1__ == self.__value2__