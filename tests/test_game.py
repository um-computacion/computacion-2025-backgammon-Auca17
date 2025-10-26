"""
Este módulo contiene las pruebas de integración para la clase Game.
"""

import unittest
from core.game import Game
from core.player import Player
from core.board import Board
from core.checker import Checker
from core.dice import Dice


class TestGame(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase Game.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada test.
        """
        self.__player1__ = Player("Alice", "white")
        self.__player2__ = Player("Bob", "black")
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__game__ = Game(
            player1=self.__player1__,
            player2=self.__player2__,
            board=self.__board__,
            dice=self.__dice__,
        )

    def test_initialization(self):
        """
        Verifica que el juego se inicializa correctamente.
        """
        self.assertIsInstance(self.__game__.__board__, Board)
        self.assertEqual(len(self.__game__.__players__), 2)
        self.assertEqual(self.__game__.__current_turn__, 0)
        self.assertIsNone(self.__game__.__winner__)

    def test_switch_turn(self):
        """
        Verifica que el turno cambia correctamente entre jugadores.
        """
        __initial_turn__ = self.__game__.__current_turn__
        self.__game__.switch_turn()
        self.assertNotEqual(self.__game__.__current_turn__, __initial_turn__)
        self.__game__.switch_turn()
        self.assertEqual(self.__game__.__current_turn__, __initial_turn__)

    def test_start_rolls_dice(self):
        """
        Verifica que el método start realiza la primera tirada de dados.
        """
        # Simulamos que los dados sacan (5, 2) y que no es un doble
        self.__game__.__dice__.get_values = lambda: (5, 2)
        self.__game__.__dice__.is_double = lambda: False

        # Llamamos a start
        self.__game__.start()

        # Verificamos que los valores de los dados se han establecido
        self.assertEqual(self.__game__.__dice_values__, [5, 2])

    def test_make_move_valid(self):
        """
        Verifica que un movimiento válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        __from_pos__ = 0 if __player__.__color__ == "white" else 23
        __to_pos__ = __from_pos__ + (3 if __player__.__color__ == "white" else -3)
        self.__game__.make_move(__from_pos__, __to_pos__)
        self.assertNotIn(3, self.__game__.__dice_values__)

    def test_make_move_invalid(self):
        """
        Verifica que un movimiento inválido lanza un ValueError.
        """
        self.__game__.start()
        self.__game__.__dice_values__ = [3, 4]
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 1)

    def test_reentry_valid(self):
        """
        Verifica que un movimiento de reingreso válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        self.__game__.__board__.get_captured(__player__.__color__).append(
            Checker(__player__.__color__)
        )
        __to_pos__ = 2 if __player__.__color__ == "white" else 20
        self.__game__.make_move(0, __to_pos__)

    def test_reentry_white_bug_fix(self):
        """
        Verifica que un jugador blanco puede reingresar desde la barra.
        """
        self.__game__.start()
        __player__ = self.__player1__
        self.__game__.__current_turn__ = 0
        self.__game__.__dice_values__ = [3, 4]
        self.__game__.__board__.get_captured(__player__.__color__).append(
            Checker(__player__.__color__)
        )
        self.__game__.make_move(0, 2)

    def test_bear_off_valid(self):
        """
        Verifica que un movimiento de sacar ficha válido se realiza con éxito.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        self.__game__.__dice_values__ = [3, 4]
        # Prepara el tablero para sacar fichas
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        if __player__.__color__ == "white":
            self.__game__.__board__.__points__[20] = [Checker(__player__.__color__)] * 2
            self.__game__.make_move(20, 24)
        else:
            self.__game__.__board__.__points__[3] = [Checker(__player__.__color__)] * 2
            self.__game__.make_move(3, -1)

    def test_win_condition(self):
        """
        Verifica que la condición de victoria se detecta correctamente.
        """
        self.__game__.start()
        __player__ = self.__game__.get_current_player()
        for i in range(15):
            self.__game__.__board__.get_home(__player__.__color__).append(
                Checker(__player__.__color__)
            )
        self.__game__.check_winner()
        self.assertEqual(self.__game__.get_winner(), __player__)

    def test_get_possible_moves_no_moves(self):
        """
        Verifica que se devuelve una lista vacía cuando no hay movimientos posibles.
        """
        # Forzar el turno del jugador blanco para hacer el test determinista
        self.__game__.__current_turn__ = 0
        self.__player__ = self.__game__.get_current_player()
        # Bloquear todos los movimientos posibles
        for i in range(6):
            color_oponente = (
                "black" if self.__player__.__color__ == "white" else "white"
            )
            # Asumiendo que el jugador blanco está en el punto 0
            # Bloquear los 6 puntos siguientes
            if self.__player__.__color__ == "white":
                self.__game__.__board__.__points__[i + 1] = [
                    Checker(color_oponente)
                ] * 2
        self.__game__.__dice_values__ = [1, 2, 3, 4, 5, 6]

        # Vaciar otros puntos para asegurar que solo el punto 0 tenga fichas
        for i in range(1, 24):
            if i > 6 or i == 0:
                self.__game__.__board__.__points__[i] = []

        # Colocar una ficha blanca en el punto 0
        if self.__player__.__color__ == "white":
            self.__game__.__board__.__points__[0] = [Checker("white")]

        __possible_moves__ = self.__game__.get_possible_moves()
        self.assertEqual(len(__possible_moves__), 0)

    def test_roll_dice_double(self):
        """
        Verifica que una tirada de dobles genera cuatro movimientos.
        Precondición: El dado se simula para que saque (3, 3).
        Resultado: La lista de valores de dados debe ser [3, 3, 3, 3].
        """
        self.__game__.__dice__.get_values = lambda: (3, 3)
        self.__game__.__dice__.is_double = lambda: True
        self.__game__.roll_dice()
        self.assertEqual(self.__game__.get_dice_values(), [3, 3, 3, 3])

    def test_can_bear_off_true(self):
        """
        Verifica que _can_bear_off devuelve True cuando todas las fichas están en casa.
        Precondición: Se mueven todas las fichas del jugador blanco a su cuadrante de casa.
        Resultado: La función debe devolver True.
        """
        player = self.__player1__  # White player
        # Limpiar el tablero
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        # Colocar todas las fichas en el cuadrante de casa
        self.__game__.__board__.__points__[18] = [Checker("white")] * 15
        self.assertTrue(self.__game__._can_bear_off(player))

    def test_can_bear_off_false(self):
        """
        Verifica que _can_bear_off devuelve False si alguna ficha está fuera de casa.
        Precondición: Una ficha del jugador blanco se deja fuera del cuadrante de casa.
        Resultado: La función debe devolver False.
        """
        player = self.__player1__  # White player
        # Dejar una ficha en el punto 0, fuera del cuadrante de casa
        self.assertFalse(self.__game__._can_bear_off(player))

    def test_is_over_after_win(self):
        """
        Verifica que is_over() devuelve True después de que un jugador gana.
        Precondición: Se establece una condición de victoria para el jugador 1.
        Resultado: is_over() debe ser True.
        """
        player = self.__player1__
        for _ in range(15):
            self.__game__.__board__.get_home(player.__color__).append(
                Checker(player.__color__)
            )
        self.__game__.check_winner()
        self.assertTrue(self.__game__.is_over())
        self.assertEqual(self.__game__.get_winner(), player)

    def test_get_possible_moves_from_bar(self):
        """
        Verifica que get_possible_moves devuelve solo movimientos de reingreso si hay fichas en la barra.
        """
        player = self.__player1__  # White player
        self.__game__.__current_turn__ = (
            0  # Asegurar que es el turno del jugador blanco
        )
        self.__game__.__board__.get_captured(player.__color__).append(
            Checker(player.__color__)
        )
        self.__game__.__dice_values__ = [2, 5]

        # El jugador blanco puede reingresar en los puntos 1 (dado 2) y 4 (dado 5)
        # Suponiendo que esos puntos no están bloqueados
        possible_moves = self.__game__.get_possible_moves()
        self.assertIn("Barra a 1", possible_moves)
        self.assertIn("Barra a 4", possible_moves)
        self.assertEqual(len(possible_moves), 2)

    def test_get_possible_moves_for_bear_off(self):
        """
        Verifica que get_possible_moves devuelve movimientos de bear off cuando es posible.
        """
        player = self.__player1__  # White player
        self.__game__.__current_turn__ = 0
        self.__game__.__dice_values__ = [3, 4]
        # Limpiar el tablero y colocar fichas en posición de bear off
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[20] = [Checker("white")]  # Mover con dado 4
        self.__game__.__board__.__points__[21] = [Checker("white")]  # Mover con dado 3

        possible_moves = self.__game__.get_possible_moves()
        self.assertIn("20 a 24", possible_moves)
        self.assertIn("21 a 24", possible_moves)

    def test_validate_move_invalid_dice(self):
        """
        Verifica que _validate_move lanza un ValueError si la distancia no coincide con los dados.
        """
        player = self.__player1__
        self.__game__.__dice_values__ = [1, 2]
        # Intentar mover 3 puntos (no disponible en los dados)
        with self.assertRaises(ValueError):
            self.__game__._validate_move(player, 0, 3)

    def test_black_player_reentry_and_dice_consumption(self):
        """
        Verifica que el jugador negro puede reingresar desde la barra y el dado se consume.
        Precondición: Ficha negra en la barra, dado de 3 disponible.
        Resultado: La ficha reingresa en el punto 21 (24 - 3) y el dado 3 se elimina.
        """
        player = self.__player2__  # Black player
        self.__game__.__current_turn__ = 1
        self.__game__.__board__.get_captured(player.__color__).append(
            Checker(player.__color__)
        )
        self.__game__.__dice_values__ = [3, 5]

        # El punto 21 debe estar libre para el reingreso
        self.__game__.__board__.__points__[21] = []

        self.__game__.make_move(0, 21)  # from_pos es irrelevante para reingreso

        self.assertEqual(len(self.__game__.__board__.get_captured(player.__color__)), 0)
        self.assertEqual(self.__game__.__board__.get_point(21)[0].__color__, "black")
        self.assertNotIn(3, self.__game__.get_dice_values())
        self.assertIn(5, self.__game__.get_dice_values())

    def test_black_player_bear_off_and_dice_consumption(self):
        """
        Verifica que el jugador negro puede hacer bear off y el dado se consume.
        Precondición: Todas las fichas negras en casa, ficha en punto 2, dado de 3.
        Resultado: La ficha sale del tablero y el dado 3 se consume.
        """
        player = self.__player2__  # Black player
        self.__game__.__current_turn__ = 1
        self.__game__.__dice_values__ = [3, 4]
        # Limpiar tablero y colocar fichas negras en su casa para permitir bear off
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[2] = [Checker("black")] * 15

        self.__game__.make_move(2, -1)  # to_pos -1 para bear off

        self.assertEqual(len(self.__game__.__board__.get_home(player.__color__)), 1)
        self.assertNotIn(3, self.__game__.get_dice_values())
        self.assertIn(4, self.__game__.get_dice_values())

    def test_validate_bear_off_invalid_dice(self):
        """
        Verifica que no se puede hacer bear off con un dado incorrecto.
        Precondición: Jugador blanco en posición de bear off, pero el dado no coincide.
        Resultado: Se lanza un ValueError.
        """
        player = self.__player1__  # White player
        self.__game__.__current_turn__ = 0
        self.__game__.__dice_values__ = [1, 2]
        # Limpiar el tablero y preparar para bear off
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[20] = [Checker("white")] * 15

        with self.assertRaises(ValueError):
            self.__game__._validate_bear_off(player, 20)

    def test_display_board_call(self):
        """
        Verifica que el método display_board se puede llamar sin errores.
        Precondición: Un juego inicializado.
        Resultado: El método se ejecuta (no se necesita assert, solo cobertura).
        """
        self.__game__.display_board()

    def test_validate_reentry_black_invalid_dice(self):
        """
        Verifica que la validación de reingreso falla para el jugador negro con un dado incorrecto.
        """
        player = self.__player2__
        self.__game__.__dice_values__ = [1, 2]
        with self.assertRaises(ValueError):
            self.__game__._validate_reentry(player, 20)  # Requiere un dado de 4

    def test_validate_move_opponent_checker(self):
        """
        Verifica que un jugador no puede mover una ficha del oponente.
        """
        player = self.__player1__  # Jugador blanco
        self.__game__.__dice_values__ = [1]
        # El punto 5 contiene fichas negras
        with self.assertRaises(ValueError):
            self.__game__._validate_move(player, 5, 6)

    def test_get_possible_moves_reentry_blocked(self):
        """
        Verifica que no hay movimientos de reingreso si los puntos están bloqueados.
        """
        player = self.__player1__  # Jugador blanco
        self.__game__.__current_turn__ = 0
        self.__game__.__board__.get_captured(player.__color__).append(
            Checker(player.__color__)
        )
        self.__game__.__dice_values__ = [1, 2]
        # Bloquear los puntos de entrada 0 y 1
        self.__game__.__board__.__points__[0] = [Checker("black")] * 2
        self.__game__.__board__.__points__[1] = [Checker("black")] * 2

        self.assertEqual(self.__game__.get_possible_moves(), [])

    def test_black_player_normal_move_dice_consumption(self):
        """
        Verifica el consumo de dado en un movimiento normal del jugador negro.
        """
        player = self.__player2__  # Jugador negro
        self.__game__.__current_turn__ = 1
        self.__game__.__dice_values__ = [3, 5]
        # Mover de 23 a 20
        self.__game__.make_move(23, 20)
        self.assertNotIn(3, self.__game__.get_dice_values())
        self.assertIn(5, self.__game__.get_dice_values())

    def test_reset_game(self):
        """
        Verifica que el juego se reinicia a su estado inicial.
        """
        # Alterar el estado del juego
        self.__game__.switch_turn()
        self.__game__.__dice_values__ = [3]  # Añadir el dado necesario
        self.__game__.make_move(23, 20)
        # Reiniciar
        self.__game__.reset()
        # Verificar estado inicial
        self.assertEqual(self.__game__.get_current_player(), self.__player1__)
        self.assertEqual(len(self.__game__.get_dice_values()), 0)

    def test_bear_off_failure_exception(self):
        """
        Verifica que se lanza ValueError si se intenta un bear off inválido.
        """
        player = self.__player1__
        self.__game__.__dice_values__ = [1]
        # Faltan fichas en casa, por lo que _can_bear_off es False
        with self.assertRaises(ValueError):
            self.__game__.make_move(20, 24)

    def test_normal_move_failure_exception(self):
        """
        Verifica que se lanza ValueError si se intenta un movimiento normal inválido.
        """
        player = self.__player1__
        self.__game__.__dice_values__ = [1]
        # Movimiento inválido (distancia incorrecta)
        with self.assertRaises(ValueError):
            self.__game__.make_move(0, 5)

    def test_get_winner_no_winner(self):
        """
        Verifica que get_winner devuelve None cuando no hay ganador.
        """
        self.assertIsNone(self.__game__.get_winner())


if __name__ == "__main__":
    unittest.main()
