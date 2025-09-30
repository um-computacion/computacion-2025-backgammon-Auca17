class Player:
    """
    Representa un jugador de Backgammon.
    """

    def __init__(self, __name__, __color__, __checkers__=None):
        """
        Inicializa un jugador con nombre, color y una lista opcional de fichas.
        :param name: Nombre del jugador.
        :param color: Color de las fichas del jugador.
        :param checkers: Lista de fichas del jugador (opcional).
        """
        self.__name__ = __name__
        self.__color__ = __color__
        self.__checkers__ = __checkers__ if __checkers__ is not None else []

    def get_name(self):
        """
        Devuelve el nombre del jugador.
        Es útil para mostrar información en la interfaz o en mensajes del juego.
        """
        return self.__name__

    def add_bar_checker(self, checker=None):
        """
        Incrementa la cantidad de fichas en la barra (fuera del tablero).
        Si se proporciona un argumento, agrega la ficha a la lista de fichas del jugador.
        Se utiliza cuando una ficha es capturada por el oponente.
        :param checker: Ficha a agregar (opcional).
        """
        if checker is not None:
            self.__checkers__.append(checker)
        else:
            # Si se usa sin argumentos, mantiene compatibilidad con lógica previa (si aplica)
            if hasattr(self, '__bar_checkers__'):
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

    def add_checker(self, __checker__):
        """
        Agrega una ficha a la lista de fichas del jugador.
        :param checker: Ficha a agregar.
        """
        self.__checkers__.append(__checker__)

    def remove_checker(self, __checker__):
        """
        Remueve una ficha de la lista de fichas del jugador si está presente.
        :param checker: Ficha a remover.
        """
        if __checker__ in self.__checkers__:
            self.__checkers__.remove(__checker__)

    @property
    def checkers(self):
        """
        Permite acceso público de solo lectura a la lista de fichas del jugador.
        Es útil para pruebas y para otras clases que necesiten consultar las fichas.
        """
        return self.__checkers__
