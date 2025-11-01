"""
Este módulo contiene las pruebas unitarias para la interfaz de línea de comandos (CLI).
"""

import unittest
from unittest.mock import patch, call, Mock
from cli import cli


class TestCLI(unittest.TestCase):
    """
    Clase de pruebas unitarias para la interfaz de línea de comandos.
    """

    @patch("builtins.input", side_effect=["Alice", "Bob"])
    def test_get_player_names(self, mock_input):
        """
        Verifica que los nombres de los jugadores se solicitan y devuelven correctamente.
        """
        # pylint: disable=protected-access
        player1_name, player2_name = cli._get_player_names()
        self.assertEqual(player1_name, "Alice")
        self.assertEqual(player2_name, "Bob")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["", " ", "Alice", "", "Bob"])
    def test_get_player_names_with_empty_input(self, mock_input):
        """
        Verifica que la función insiste hasta que se ingresan nombres no vacíos.
        """
        # pylint: disable=protected-access
        player1_name, player2_name = cli._get_player_names()
        self.assertEqual(player1_name, "Alice")
        self.assertEqual(player2_name, "Bob")
        self.assertEqual(mock_input.call_count, 5)

    @patch("random.randint", side_effect=[6, 1])
    @patch("builtins.print")
    def test_decide_first_player_p1_wins(self, _mock_print, _mock_randint):
        """
        Verifica que el jugador 1 empieza si saca un dado más alto.
        """
        # pylint: disable=protected-access
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 0)

    @patch("random.randint", side_effect=[2, 5])
    @patch("builtins.print")
    def test_decide_first_player_p2_wins(self, _mock_print, _mock_randint):
        """
        Verifica que el jugador 2 empieza si saca un dado más alto.
        """
        # pylint: disable=protected-access
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 1)

    @patch("random.randint", side_effect=[3, 3, 5, 4])
    @patch("builtins.input", return_value=None)
    @patch("builtins.print")
    def test_decide_first_player_tie(self, _mock_print, _mock_input, mock_randint):
        """
        Verifica que se vuelve a tirar el dado en caso de empate.
        """
        # pylint: disable=protected-access
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 0)
        self.assertEqual(mock_randint.call_count, 4)

    @patch("builtins.print")
    def test_display_possible_moves(self, mock_print):
        """
        Verifica que la lista de movimientos posibles se muestra correctamente.
        """
        moves = ["0 a 1", "Barra a 5", "sacar 24"]
        # pylint: disable=protected-access
        cli._display_possible_moves(moves)
        mock_print.assert_has_calls(
            [
                call("Movimientos posibles:"),
                call("1) 1 a 2"),
                call("2) Barra a 6"),
                call("3) Sacar 24"),
            ]
        )

    @patch("builtins.print")
    def test_display_possible_moves_empty(self, mock_print):
        """
        Verifica que no se muestra nada si la lista de movimientos está vacía.
        """
        # pylint: disable=protected-access
        cli._display_possible_moves([])
        mock_print.assert_not_called()

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "11 16", "11 18", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_game_flow(
        self, mock_print, mock_game_cls, _mock_input, mock_decide, mock_get_names
    ):
        """
        Verifica el flujo principal del juego, incluyendo movimientos y salida.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, False, True]
        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player
        mock_game_instance.get_dice_values.return_value = [5, 2]
        mock_game_instance.get_possible_moves.return_value = ["11 a 16", "11 a 18"]
        mock_game_instance.make_move.side_effect = [True, True]
        mock_game_instance.get_winner.return_value.get_player_name.return_value = (
            "Alice"
        )

        cli.main()

        mock_get_names.assert_called_once()
        mock_decide.assert_called_once_with("Alice", "Bob")
        mock_game_instance.make_move.assert_has_calls(
            [
                call(10, 15),
                call(10, 17),
            ]
        )
        self.assertIn(
            call("\n¡Juego terminado! ¡Alice gana!"), mock_print.call_args_list
        )

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "invalid move", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_invalid_move_format(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el manejo de un formato de movimiento inválido.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]

        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player

        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = ["0 a 1"]
        # Simulamos que el jugador está en fase de reingreso para probar el mensaje de ayuda.
        mock_game_instance.current_player_has_captured.return_value = True
        mock_game_instance.can_current_player_bear_off.return_value = False

        cli.main()

        self.assertIn(
            call("Entrada inválida. Asegúrate de usar el formato correcto."),
            mock_print.call_args_list,
        )

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "1 6", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_failed_move(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el manejo de un movimiento que falla en la lógica del juego.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]

        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player

        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = ["0 a 1"]
        mock_game_instance.make_move.return_value = False

        cli.main()

        mock_game_instance.make_move.assert_called_once_with(0, 5)
        self.assertIn(call("Movimiento inválido."), mock_print.call_args_list)

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=[""])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_no_possible_moves(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el flujo cuando un jugador no tiene movimientos posibles.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, True, True]
        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = []

        cli.main()
        self.assertIn(
            call("No tienes movimientos posibles. El turno pasa al siguiente jugador."),
            mock_print.call_args_list,
        )
        mock_game_instance.switch_turn.assert_called_once()

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "5", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_reentry_flow(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el flujo de reingreso con un solo número.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]

        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player

        # Simulamos que el jugador tiene una ficha capturada
        mock_game_instance.current_player_has_captured.return_value = True
        mock_game_instance.get_dice_values.return_value = [5, 2]
        mock_game_instance.get_possible_moves.return_value = ["Barra a 4", "Barra a 1"]
        mock_game_instance.make_move.return_value = True

        cli.main()

        # Verificamos que se llamó a make_move con -1 (desde la barra) y el destino correcto (4)
        mock_game_instance.make_move.assert_called_once_with(-1, 4)
        self.assertIn(call("Movimiento exitoso."), mock_print.call_args_list)

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "sacar 24", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_bear_off_flow_simplified(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el flujo de bear-off con el comando 'sacar'.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]

        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player

        mock_game_instance.current_player_has_captured.return_value = False
        mock_game_instance.can_current_player_bear_off.return_value = True
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = ["sacar 24"]
        mock_game_instance.make_move.return_value = True

        cli.main()

        # Verificamos que se llamó a make_move con la posición correcta para el bear-off (23)
        # y el destino especial para bear-off de blancas (24).
        mock_game_instance.make_move.assert_called_once_with(23, 24)
        self.assertIn(call("Ficha retirada con éxito."), mock_print.call_args_list)

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "invalid format", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_invalid_move_format_bear_off(
        self, mock_print, mock_game_cls, _mock_input, _mock_decide, _mock_get_names
    ):
        """
        Verifica el mensaje de ayuda contextual para un formato inválido durante el bear-off.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]

        mock_player = Mock()
        mock_player.get_player_name.return_value = "Alice"
        mock_player.__color__ = "white"
        mock_game_instance.get_current_player.return_value = mock_player

        mock_game_instance.current_player_has_captured.return_value = False
        mock_game_instance.can_current_player_bear_off.return_value = True
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = ["sacar 24"]

        cli.main()

        mock_print.assert_has_calls(
            [
                call("Recuerda: para retirar una ficha, escribe 'sacar [número]'."),
            ]
        )


if __name__ == "__main__":
    unittest.main()
