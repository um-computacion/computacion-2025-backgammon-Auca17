class Checker:
    """
    Attributes:
        __color__ (str): Color o identificador del jugador propietario.
        __position__ (int or str): Posición actual en el tablero (punto, 'bar', 'borne').
        __is_captured__ (bool): Indica si la ficha está capturada.
    """

    def __init__(self, color):
        """
        Inicializa una ficha con color.

        Args:
            color (str): Color del jugador.
        """
        if color not in ("white", "black"):
            raise ValueError("Color must be 'white' or 'black'")
        self.__color__ = color
        self.__position__ = None
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
        self.__position__ = "bar"

    def __repr__(self):
        # Representación textual de la ficha, útil para depuración
        return f"Checker({self.__color__})"
