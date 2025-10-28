"""
Este módulo contiene las pruebas unitarias para la interfaz de línea de comandos (CLI).
"""

import unittest
from unittest.mock import patch, call
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
        player1_name, player2_name = cli._get_player_names()
        self.assertEqual(player1_name, "Alice")
        self.assertEqual(player2_name, "Bob")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["", " ", "Alice", "", "Bob"])
    def test_get_player_names_with_empty_input(self, mock_input):
        """
        Verifica que la función insiste hasta que se ingresan nombres no vacíos.
        """
        player1_name, player2_name = cli._get_player_names()
        self.assertEqual(player1_name, "Alice")
        self.assertEqual(player2_name, "Bob")
        self.assertEqual(mock_input.call_count, 5)

    @patch("random.randint", side_effect=[6, 1])
    @patch("builtins.print")
    def test_decide_first_player_p1_wins(self, mock_print, mock_randint):
        """
        Verifica que el jugador 1 empieza si saca un dado más alto.
        """
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 0)

    @patch("random.randint", side_effect=[2, 5])
    @patch("builtins.print")
    def test_decide_first_player_p2_wins(self, mock_print, mock_randint):
        """
        Verifica que el jugador 2 empieza si saca un dado más alto.
        """
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 1)

    @patch("random.randint", side_effect=[3, 3, 5, 4])
    @patch("builtins.input", return_value=None)
    @patch("builtins.print")
    def test_decide_first_player_tie(self, mock_print, mock_input, mock_randint):
        """
        Verifica que se vuelve a tirar el dado en caso de empate.
        """
        winner_idx = cli._decide_first_player("Alice", "Bob")
        self.assertEqual(winner_idx, 0)
        self.assertEqual(mock_randint.call_count, 4)

    @patch("builtins.print")
    def test_display_possible_moves(self, mock_print):
        """
        Verifica que la lista de movimientos posibles se muestra correctamente.
        """
        moves = [(0, 1), (1, 2)]
        cli._display_possible_moves(moves)
        mock_print.assert_has_calls(
            [
                call("Movimientos posibles:"),
                call("1) (0, 1)"),
                call("2) (1, 2)"),
            ]
        )

    @patch("builtins.print")
    def test_display_possible_moves_empty(self, mock_print):
        """
        Verifica que no se muestra nada si la lista de movimientos está vacía.
        """
        cli._display_possible_moves([])
        mock_print.assert_not_called()

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "11 16", "11 18", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_game_flow(
        self, mock_print, mock_game_cls, mock_input, mock_decide, mock_get_names
    ):
        """
        Verifica el flujo principal del juego, incluyendo movimientos y salida.
        """
        # Configuramos el mock de la instancia del juego
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, False, True]
        mock_game_instance.get_current_player.return_value.get_name.return_value = (
            "Alice"
        )
        mock_game_instance.get_current_player.return_value.__color__ = "white"
        mock_game_instance.get_dice_values.return_value = [5, 2]
        mock_game_instance.get_possible_moves.return_value = [(11, 16), (11, 18)]
        mock_game_instance.make_move.side_effect = [True, True]
        mock_game_instance.get_winner.return_value.get_name.return_value = "Alice"

        cli.main()

        # Verificamos que las funciones iniciales fueron llamadas
        mock_get_names.assert_called_once()
        mock_decide.assert_called_once_with("Alice", "Bob")

        # Verificamos que se intentaron los movimientos
        mock_game_instance.make_move.assert_has_calls(
            [
                call(11, 16),
                call(11, 18),
            ]
        )

        # Verificamos que el mensaje de victoria se muestra
        self.assertIn(
            call("\n¡Juego terminado! ¡Alice gana!"), mock_print.call_args_list
        )

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "invalid move", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_invalid_move_format(
        self, mock_print, mock_game_cls, mock_input, mock_decide, mock_get_names
    ):
        """
        Verifica el manejo de un formato de movimiento inválido.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]
        mock_game_instance.get_current_player.return_value.get_name.return_value = (
            "Alice"
        )
        mock_game_instance.get_current_player.return_value.__color__ = "white"
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = [(0, 1)]

        cli.main()

        self.assertIn(
            call("Formato de entrada inválido. Usa 'desde hasta'."),
            mock_print.call_args_list,
        )

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=["", "0 5", "salir"])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_failed_move(
        self, mock_print, mock_game_cls, mock_input, mock_decide, mock_get_names
    ):
        """
        Verifica el manejo de un movimiento que falla en la lógica del juego.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, False, True]
        mock_game_instance.get_current_player.return_value.get_name.return_value = (
            "Alice"
        )
        mock_game_instance.get_current_player.return_value.__color__ = "white"
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = [(0, 1)]
        mock_game_instance.make_move.return_value = False

        cli.main()

        mock_game_instance.make_move.assert_called_once_with(0, 5)
        self.assertIn(
            call("Movimiento inválido. Inténtalo de nuevo."), mock_print.call_args_list
        )

    @patch("cli.cli._get_player_names", return_value=("Alice", "Bob"))
    @patch("cli.cli._decide_first_player", return_value=0)
    @patch("builtins.input", side_effect=[""])
    @patch("cli.cli.Game")
    @patch("builtins.print")
    def test_main_no_possible_moves(
        self, mock_print, mock_game_cls, mock_input, mock_decide, mock_get_names
    ):
        """
        Verifica el flujo cuando un jugador no tiene movimientos posibles.
        """
        mock_game_instance = mock_game_cls.return_value
        mock_game_instance.is_over.side_effect = [False, True, True]
        mock_game_instance.get_current_player.return_value.get_name.return_value = (
            "Alice"
        )
        mock_game_instance.get_current_player.return_value.__color__ = "white"
        mock_game_instance.get_dice_values.return_value = [1, 2]
        mock_game_instance.get_possible_moves.return_value = []

        cli.main()
        self.assertIn(
            call("No tienes movimientos posibles. El turno pasa al siguiente jugador."),
            mock_print.call_args_list,
        )
        mock_game_instance.switch_turn.assert_called_once()


if __name__ == "__main__":
    unittest.main()
