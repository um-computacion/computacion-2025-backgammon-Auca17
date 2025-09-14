class Board:
    def __init__(self):
        # El tablero tiene 24 puntos (triángulos)
        self.__points__ = [None for _ in range(24)]
        # La barra central separa ambos lados
        self.__bar__ = None
        # Lados del tablero
        self.__left_side__ = self.__points__[:12]
        self.__right_side__ = self.__points__[12:]

    def display(self):
        print("Backgammon Board:")
        print("Left Side:", self.__left_side__)
        print("Bar:", self.__bar__)
        print("Right Side:", self.__right_side__)