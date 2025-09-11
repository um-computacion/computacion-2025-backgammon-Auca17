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
        self.color = color
        self.position = position
        self.is_captured = False

    def move_to(self, new_position):
        """
        Mueve la ficha a una nueva posición.

        Args:
            new_position (int or str): Nueva posición.
        """
        self.position = new_position

    def capture(self):
        """
        Captura la ficha y la envía al 'bar'.
        """
        self.is_captured = True
        self.position = 'bar'