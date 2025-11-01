"""
Módulo principal del juego Backgammon.

Este módulo contiene la clase Game que gestiona toda la lógica del juego,
incluyendo turnos, movimientos, validaciones y condiciones de victoria.
Coordina la interacción entre el tablero, los jugadores y los dados.

Classes
-------
Game
    Clase principal que controla el flujo del juego Backgammon
"""


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

    def __init__(self, player1, player2, board, dice):
        """
        Inicializa el juego con dos jugadores y las dependencias del tablero y los dados.

        Args:
            player1 (Player): El primer jugador.
            player2 (Player): El segundo jugador.
            board (Board): La instancia del tablero de juego.
            dice (Dice): La instancia de los dados.
        """
        self.__players__ = [player1, player2]
        self.__current_turn__ = 0
        self.__history__ = []
        self.__winner__ = None
        self.__board__ = board
        self.__dice__ = dice
        self.__dice_values__ = []

    def start(self):
        """
        Realiza la primera tirada de dados para el jugador inicial.
        """
        self.roll_dice()

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
        self.__board__.__init__()  # Reinicia el tablero a su estado inicial
        self.__current_turn__ = 0
        self.__history__ = []
        self.__winner__ = None
        self.__dice_values__ = []
        self.start()  # Realiza la primera tirada de dados

    def get_current_player(self):
        """
        Devuelve el jugador actual.
        """
        return self.__players__[self.__current_turn__]

    def current_player_has_captured(self):
        """
        Verifica si el jugador actual tiene fichas capturadas.
        """
        __player__ = self.get_current_player()
        return len(self.__board__.get_captured(__player__.__color__)) > 0

    def can_current_player_bear_off(self):
        """
        Verifica si el jugador actual puede empezar a sacar fichas.
        """
        __player__ = self.get_current_player()
        return self._can_bear_off(__player__)

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

    def get_possible_moves(self):
        """
        Calcula y devuelve una lista de todos los movimientos posibles para el jugador actual.
        Delega la lógica a métodos helper según el estado del juego.
        """
        __player__ = self.get_current_player()

        if self.__board__.get_captured(__player__.__color__):
            return self._get_reentry_moves()
        if self.can_current_player_bear_off():
            # Cuando se puede hacer bear off, se deben considerar tanto
            # los movimientos normales como los de sacar fichas.
            normal_moves = self._get_normal_moves()
            bear_off_moves = self._get_bear_off_moves()
            return normal_moves + bear_off_moves

        return self._get_normal_moves()

    def _get_reentry_moves(self):
        """Calcula los movimientos de reingreso posibles desde la barra."""
        __possible_moves__ = []
        __player__ = self.get_current_player()
        __dice__ = self.get_dice_values()
        for __die__ in set(__dice__):
            try:
                __to_pos__ = (
                    __die__ - 1 if __player__.__color__ == "white" else 24 - __die__
                )
                if self._validate_reentry(__player__, __to_pos__):
                    __possible_moves__.append(f"Barra a {__to_pos__}")
            except (ValueError, TypeError):  # Añadido TypeError
                continue
        return __possible_moves__

    def _get_bear_off_moves(self):
        """
        Calcula y devuelve todos los movimientos de bear-off válidos, incluyendo
        movimientos exactos y la regla del 'overshoot'.
        """
        possible_moves = []
        player = self.get_current_player()
        dice_values = set(self.get_dice_values())
        home_board_range = range(18, 24) if player.__color__ == "white" else range(6)

        # 1. Movimientos exactos
        for from_pos in home_board_range:
            if (
                self.__board__.get_point_count(from_pos) > 0
                and self.__board__.get_point(from_pos)[-1].__color__ == player.__color__
            ):
                for die in dice_values:
                    try:
                        if self._validate_bear_off(player, from_pos, die):
                            possible_moves.append(f"sacar {from_pos + 1}")
                    except (ValueError, IndexError):
                        continue

        # 2. Regla del 'overshoot'
        # Si un dado es mayor que la ficha de mayor numeración y no hay otros
        # movimientos posibles para ese dado, se puede usar para sacar esa ficha.
        highest_checker_pos = -1
        if player.__color__ == "white":
            for pos in range(18, 24):  # 18 to 23
                if (
                    self.__board__.get_point_count(pos) > 0
                    and self.__board__.get_point(pos)[-1].__color__ == player.__color__
                ):
                    highest_checker_pos = pos
                    break
        else:  # Black
            for pos in range(6):  # 0 to 5
                if (
                    self.__board__.get_point_count(pos) > 0
                    and self.__board__.get_point(pos)[-1].__color__ == player.__color__
                ):
                    highest_checker_pos = pos
                    break

        if highest_checker_pos != -1:
            for die in dice_values:
                is_exact_move_possible_for_die = False
                for from_pos in home_board_range:
                    if (
                        player.__color__ == "white"
                        and 24 - from_pos == die
                        and self.__board__.get_point_count(from_pos) > 0
                    ):
                        is_exact_move_possible_for_die = True
                        break
                    if (
                        player.__color__ == "black"
                        and from_pos + 1 == die
                        and self.__board__.get_point_count(from_pos) > 0
                    ):
                        is_exact_move_possible_for_die = True
                        break

                if not is_exact_move_possible_for_die:
                    try:
                        if self._validate_bear_off(player, highest_checker_pos, die):
                            move_str = f"sacar {highest_checker_pos + 1}"
                            if move_str not in possible_moves:
                                possible_moves.append(move_str)
                    except (ValueError, IndexError):
                        continue

        return list(set(possible_moves))

    def _get_normal_moves(self):
        """Calcula los movimientos normales posibles en el tablero."""
        __possible_moves__ = []
        __player__ = self.get_current_player()
        __dice__ = self.get_dice_values()
        for __from_pos__ in range(24):
            if (
                self.__board__.get_point_count(__from_pos__) > 0
                and self.__board__.get_point(__from_pos__)[-1].__color__
                == __player__.__color__
            ):
                for __die__ in set(__dice__):
                    try:
                        __direction__ = 1 if __player__.__color__ == "white" else -1
                        __to_pos__ = __from_pos__ + __die__ * __direction__
                        if 0 <= __to_pos__ < 24:
                            if self._validate_move(
                                __player__, __from_pos__, __to_pos__
                            ):
                                __possible_moves__.append(
                                    f"{__from_pos__} a {__to_pos__}"
                                )
                    except (ValueError, IndexError):
                        continue
        return __possible_moves__

    def get_dice_values(self):
        """
        Devuelve los valores actuales de los dados.
        """
        return self.__dice_values__

    def display_board(self):
        """
        Muestra el estado actual del tablero en una representación 2D.
        """
        print(self.__board__.get_2d_representation())

    def _validate_reentry(self, __player__, __to_pos__):
        """
        Valida el movimiento de reingreso de un jugador.
        """
        if __player__.__color__ == "white":
            if __to_pos__ + 1 not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")
        else:  # black
            if 24 - __to_pos__ not in self.__dice_values__:
                raise ValueError("La distancia del movimiento no coincide con el dado")

        if (
            self.__board__.get_point_count(__to_pos__) > 1
            and self.__board__.get_point(__to_pos__)[-1].__color__
            != __player__.__color__
        ):
            raise ValueError("El punto de destino está bloqueado")

        return True

    def _can_bear_off(self, __player__):
        """
        Verifica si un jugador puede empezar a sacar fichas.
        """
        # El home board de las blancas son los puntos 18-23 (visual 19-24).
        # El de las negras son los puntos 0-5 (visual 1-6).
        __home_points__ = range(18, 24) if __player__.__color__ == "white" else range(6)

        # Todas las fichas deben estar en el cuadrante de casa
        for i in range(24):
            if i not in __home_points__:
                if (
                    self.__board__.get_point_count(i) > 0
                    and len(self.__board__.get_point(i)) > 0
                    and self.__board__.get_point(i)[-1].__color__
                    == __player__.__color__
                ):
                    return False
        return True

    def _validate_bear_off(self, player, from_pos, die):
        """
        Valida un movimiento de bear-off, incluyendo la regla del 'overshoot'.
        """
        if not self._can_bear_off(player):
            raise ValueError(
                "No se pueden sacar fichas hasta que todas estén en el cuadrante de casa."
            )

        # 1. Validar que hay una ficha del jugador en esa posición
        if not (0 <= from_pos < 24):
            raise IndexError("El punto está fuera de los límites del tablero")
        if self.__board__.get_point_count(from_pos) == 0:
            raise ValueError("No hay fichas en el punto de origen.")
        if self.__board__.get_point(from_pos)[-1].__color__ != player.__color__:
            raise ValueError("El jugador no es dueño de la ficha.")

        # 2. Regla del movimiento exacto
        is_exact_move = False
        if player.__color__ == "white" and 24 - from_pos == die:
            is_exact_move = True
        elif player.__color__ == "black" and from_pos + 1 == die:
            is_exact_move = True

        if is_exact_move:
            return True

        # 3. Regla del "Overshoot"
        highest_checker_pos = -1
        if player.__color__ == "white":
            for pos in range(18, 24):  # 18 to 23
                if (
                    self.__board__.get_point_count(pos) > 0
                    and self.__board__.get_point(pos)[-1].__color__ == player.__color__
                ):
                    highest_checker_pos = pos
                    break
        else:  # Black
            for pos in range(6):  # 0 to 5
                if (
                    self.__board__.get_point_count(pos) > 0
                    and self.__board__.get_point(pos)[-1].__color__ == player.__color__
                ):
                    highest_checker_pos = pos
                    break

        # El "overshoot" es válido si la ficha está en la posición más alta
        # y el dado es mayor que la distancia necesaria para sacarla.
        if from_pos == highest_checker_pos:
            if player.__color__ == "white" and die > 24 - from_pos:
                return True
            if player.__color__ == "black" and die > from_pos + 1:
                return True

        raise ValueError("Movimiento de bear-off inválido.")

    def _validate_move(self, __player__, __from_pos__, __to_pos__):
        """
        Valida un movimiento normal de un jugador en el tablero.
        """
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

        if (
            self.__board__.get_point_count(__to_pos__) > 1
            and self.__board__.get_point(__to_pos__)[-1].__color__
            != __player__.__color__
        ):
            raise ValueError("El punto de destino está bloqueado")

        return True

    def make_move(self, __from_pos__, __to_pos__):
        """
        Realiza un movimiento en el tablero si es válido.
        Delega la ejecución a métodos helper según el tipo de movimiento.
        """
        __player__ = self.get_current_player()
        is_bear_off = __to_pos__ in (24, -1)
        is_reentry = self.current_player_has_captured()

        if is_reentry:
            return self._execute_reentry_move(__player__, __to_pos__)
        if is_bear_off:
            return self._execute_bear_off(__player__, __from_pos__)

        return self._execute_board_move(__player__, __from_pos__, __to_pos__)

    def _execute_reentry_move(self, __player__, __to_pos__):
        """Ejecuta un movimiento de reingreso desde la barra."""
        try:
            if self._validate_reentry(__player__, __to_pos__):
                self.__board__.enter_from_captured(__player__.__color__, __to_pos__)
                if __player__.__color__ == "white":
                    self.__dice_values__.remove(__to_pos__ + 1)
                else:  # black
                    self.__dice_values__.remove(24 - __to_pos__)

                if not self.__dice_values__:
                    self.switch_turn()
                return True
        except (ValueError, IndexError):
            return False
        return False

    def _execute_bear_off(self, __player__, __from_pos__):
        """Ejecuta el movimiento de sacar una ficha (bear off)."""
        die = -1
        if __player__.__color__ == "white":
            die = 24 - __from_pos__
        else:  # black
            die = __from_pos__ + 1

        if die not in self.__dice_values__:
            return False  # No se puede usar un dado que no se tiene

        try:
            if self._validate_bear_off(__player__, __from_pos__, die):
                self.__board__.bear_off(__player__.__color__, __from_pos__)
                self.__dice_values__.remove(die)
                self.check_winner()
                if not self.__dice_values__ and not self.is_over():
                    self.switch_turn()
                return True
        except (ValueError, IndexError):
            return False  # Movimiento inválido
        return False

    def _execute_board_move(self, __player__, __from_pos__, __to_pos__):
        """Ejecuta un movimiento normal en el tablero."""
        try:
            if self._validate_move(__player__, __from_pos__, __to_pos__):
                self.__board__.move_checker(
                    __player__.__color__, __from_pos__, __to_pos__
                )
                __direction__ = 1 if __player__.__color__ == "white" else -1
                __move_distance__ = (__to_pos__ - __from_pos__) * __direction__
                self.__dice_values__.remove(__move_distance__)

                self.check_winner()
                if not self.__dice_values__ and not self.is_over():
                    self.switch_turn()
                return True
        except (ValueError, IndexError):
            return False
        return False
