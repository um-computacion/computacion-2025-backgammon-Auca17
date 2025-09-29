class Player:
    def __init__(self, name):
        self.name = name
        self.checkers_off = 0  # Simplified: track checkers borne off

    def get_name(self):
        """
        Devuelve el nombre del jugador.
        Es útil para mostrar información en la interfaz o en mensajes del juego.
        """
        return self.__name__

    def add_bar_checker(self):
        """
        Incrementa la cantidad de fichas en la barra (fuera del tablero).
        Se utiliza cuando una ficha es capturada por el oponente.
        """
        self.__bar_checkers__ += 1

    def remove_bar_checker(self):
        """
        Decrementa la cantidad de fichas en la barra.
        Se utiliza cuando el jugador reingresa una ficha al tablero.
        """
        if self.__bar_checkers__ > 0:
            self.__bar_checkers__ -= 1

    def add_home_checker(self):
        """
        Incrementa la cantidad de fichas en casa (fuera del tablero, ya ganadas).
        Se utiliza cuando el jugador logra sacar una ficha del tablero.
        """
        self.__home_checkers__ += 1

    def get_bar_checkers(self):
        """
        Devuelve la cantidad de fichas en la barra.
        Permite a otras clases (como Game) verificar si el jugador tiene fichas fuera.
        """
        return self.__bar_checkers__

    def get_home_checkers(self):
        """
        Devuelve la cantidad de fichas en casa.
        Permite verificar si el jugador está cerca de ganar.
        """
        return self.__home_checkers__
