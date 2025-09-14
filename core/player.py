class Player:
    def __init__(self, __name__, __color__):
        self.__name__ = __name__          # Nombre del jugador
        self.__color__ = __color__        # Color de fichas (por ejemplo, 'blanco' o 'negro')
        self.__pieces__ = 15              # Número de fichas iniciales
        self.__bar__ = 0                  # Fichas en la barra (capturadas)
        self.__home__ = 0                 # Fichas en casa (ya retiradas del tablero)
        self.__moves__ = []               # Historial de movimientos

    def __str__(self):
        return f"Player({self.__name__}, {self.__color__})"

    def move_piece(self, from_pos, to_pos):
        # Lógica para mover una ficha
        pass

    def add_to_bar(self):
        # Lógica para agregar una ficha a la barra
        pass

    def bear_off(self):
        # Lógica para retirar una ficha del tablero
        pass

    def reset(self):
        # Reinicia los atributos para una nueva partida
        pass
