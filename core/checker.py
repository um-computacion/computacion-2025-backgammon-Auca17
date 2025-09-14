class Checker:
    """
    Attributes:
        color (str): Color o identificador del jugador propietario.
        position (int or str): Posición actual en el tablero (punto, 'bar', 'borne').
        is_captured (bool): Indica si la ficha está capturada.
    """

    def __init__(self, color, position):
        """
        Inicializa una ficha con color y posición.

        Args:
            color (str): Color del jugador.
            position (int or str): Posición inicial.
        """
        self.__color__ = color
        self.__position__ = position
        self.__is_captured__ = False

    def move_to(self, new_position):
        """
        Mueve la ficha a una nueva posición.

        Args:
            new_position (int or str): Nueva posición.
        """
        self.__position__ = new_position

    def capture(self):
        """
        Captura la ficha y la envía al 'bar'.
        """
        self.__is_captured__ = True
        self.__position__ = 'bar'