from core.board import Board
from core.player import Player
from core.dice import Dice


class Game:
    """
    Gestiona el flujo de un juego de Backgammon, conectando el tablero, los jugadores y las reglas.

    Atributos:
        __players__ (list): Una lista de los dos jugadores en el juego.
        __current_turn__ (int): El índice del jugador actual en la lista __players__.
        __history__ (list): Un historial de los movimientos realizados en el juego.
        __winner__ (Player): El ganador del juego.
        __board__ (Board): El tablero del juego.
        __dice__ (Dice): Los dados utilizados en el juego.
        __dice_values__ (list): Los valores actuales de los dados.
    """

    def __init__(self, __player1__=None, __player2__=None):
        """
        Inicializa el juego con dos jugadores.

        Si no se proporcionan jugadores, se crean jugadores por defecto.

        Args:
            __player1__ (Player, optional): El primer jugador. Por defecto es None.
            __player2__ (Player, optional): El segundo jugador. Por defecto es None.
        """
        if __player1__ is None:
            __player1__ = Player("Jugador1", "white")
        if __player2__ is None:
            __player2__ = Player("Jugador2", "black")
        self.__players__ = [__player1__, __player2__]
        self.__current_turn__ = 0
        self.__history__ = []
        self.__winner__ = None
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__dice_values__ = []

    def start(self):
        """
        Inicia el juego y determina el primer turno lanzando los dados.
        """
        while True:
            self.__dice__.roll()
            __values__ = self.__dice__.get_values()
            if __values__[0] != __values__[1]:
                self.__current_turn__ = 0 if __values__[0] > __values__[1] else 1
                self.__dice_values__ = list(__values__)
                break

    def switch_turn(self):
        """
        Cambia el turno al siguiente jugador y lanza los dados.
        """
        self.__current_turn__ = 1 - self.__current_turn__
        self.roll_dice()

    def roll_dice(self):
        """
        Lanza los dados y establece los valores para el turno actual.
        """
        self.__dice__.roll()
        __values__ = self.__dice__.get_values()
        if self.__dice__.is_double():
            self.__dice_values__ = [__values__[0]] * 4
        else:
            self.__dice_values__ = list(__values__)

    def check_winner(self):
        """
        Verifica si algún jugador ha ganado la partida.
        """
        for __player__ in self.__players__:
            if len(self.__board__.get_home(__player__.__color__)) == 15:
                self.__winner__ = __player__
                break

    def reset(self):
        """
        Reinicia el juego para una nueva partida.
        """
        self.__init__(self.__players__[0], self.__players__[1])


    def get_current_player(self):
        """
        Devuelve el jugador actual.
        """
        return self.__players__[self.__current_turn__]

    def is_over(self):
        """
        Verifica si el juego ha terminado.
        """
        return self.__winner__ is not None

    def get_winner(self):
        """
        Devuelve el ganador del juego.
        """
        return self.__winner__

    def get_dice_values(self):
        """
        Devuelve los valores actuales de los dados.
        """
        return self.__dice_values__

    def display_board(self):
        """
        Muestra el estado actual del tablero.
        """
        print("Tablero: " + " ".join(str(x["count"]) for x in self.__board__.__points_status__))

    def _validate_reentry(self, __player__, __to_pos__):
        """
        Valida el movimiento de reingreso de un jugador.
        """
        if __player__.__color__ == "white":
            if __to_pos__ + 1 not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")
        else: # black
            if 24 - __to_pos__ not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")

        if self.__board__.get_point_count(__to_pos__) > 1 and self.__board__.get_point(__to_pos__)[-1].__color__ != __player__.__color__:
            raise ValueError("El punto de destino está bloqueado")

        return True

    def _can_bear_off(self, __player__):
        """
        Verifica si un jugador puede empezar a sacar fichas.
        """
        __home_points__ = range(18, 24) if __player__.__color__ == "white" else range(6)
        
        # Todas las fichas deben estar en el cuadrante de casa
        for i in range(24):
            if i not in __home_points__:
                if self.__board__.get_point_count(i) > 0 and self.__board__.get_point(i)[-1].__color__ == __player__.__color__:
                    return False
        return True

    def _validate_bear_off(self, __player__, __from_pos__):
        """
        Valida el movimiento de sacar una ficha de un jugador.
        """
        if not self._can_bear_off(__player__):
            raise ValueError("No se pueden sacar fichas hasta que todas estén en el cuadrante de casa")

        if __player__.__color__ == "white":
            if 24 - __from_pos__ not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")
        else: # black
            if __from_pos__ + 1 not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")

        return True
    
    def _validate_move(self, __player__, __from_pos__, __to_pos__):
        """
        Valida el movimiento de un jugador.
        """
        if self.__board__.get_captured(__player__.__color__):
            return self._validate_reentry(__player__, __to_pos__)

        if not (0 <= __from_pos__ < 24 and 0 <= __to_pos__ < 24):
            raise IndexError("El punto está fuera de los límites del tablero")

        __direction__ = 1 if __player__.__color__ == "white" else -1
        __move_distance__ = (__to_pos__ - __from_pos__) * __direction__

        if __move_distance__ not in self.__dice_values__:
            raise ValueError("La distancia del movimiento no coincide con el dado")

        if self.__board__.get_point_count(__from_pos__) == 0:
            raise ValueError("No hay fichas en el punto de origen")

        if self.__board__.get_point(__from_pos__)[-1].__color__ != __player__.__color__:
            raise ValueError("El jugador no es dueño de la ficha")

        if self.__board__.get_point_count(__to_pos__) > 1 and self.__board__.get_point(__to_pos__)[-1].__color__ != __player__.__color__:
            raise ValueError("El punto de destino está bloqueado")

        return True

    def make_move(self, __from_pos__, __to_pos__):
        """
        Realiza un movimiento en el tablero si es válido.
        """
        __player__ = self.get_current_player()
        
        # Lógica para sacar fichas (bear off)
        # Para blanco, to_pos es 24. Para negro, to_pos es -1.
        if __to_pos__ == 24 or __to_pos__ == -1:
            if self._validate_bear_off(__player__, __from_pos__):
                self.__board__.bear_off(__player__.__color__, __from_pos__)
                if __player__.__color__ == "white":
                    self.__dice_values__.remove(24 - __from_pos__)
                else: # black
                    self.__dice_values__.remove(__from_pos__ + 1)
                
                self.check_winner()
                if not self.__dice_values__ and not self.is_over():
                    self.switch_turn()
                return True
        # Lógica para movimientos normales o reingreso
        elif self._validate_move(__player__, __from_pos__, __to_pos__):
            # Si hay fichas capturadas, el movimiento es un reingreso
            if self.__board__.get_captured(__player__.__color__):
                self.__board__.enter_from_captured(__player__.__color__, __to_pos__)
                if __player__.__color__ == "white":
                    self.__dice_values__.remove(__to_pos__ + 1)
                else: # black
                    self.__dice_values__.remove(24 - __to_pos__)
            # Movimiento normal
            else:
                self.__board__.move_checker(__player__.__color__, __from_pos__, __to_pos__)
                __direction__ = 1 if __player__.__color__ == "white" else -1
                __move_distance__ = (__to_pos__ - __from_pos__) * __direction__
                self.__dice_values__.remove(__move_distance__)
            
            self.check_winner()
            if not self.__dice_values__ and not self.is_over():
                self.switch_turn()
            return True
        
        return False
