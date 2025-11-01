"""
Módulo principal para la interfaz de línea de comandos del juego Backgammon.
"""

import random
from core.game import Game
from core.player import Player
from core.board import Board
from core.dice import Dice


def _get_player_names():
    """Solicita y valida los nombres de los jugadores."""
    player1_name = ""
    while not player1_name.strip():
        player1_name = input("Nombre del Jugador 1 (fichas blancas): ")

    player2_name = ""
    while not player2_name.strip():
        player2_name = input("Nombre del Jugador 2 (fichas negras): ")

    return player1_name, player2_name


def _decide_first_player(player1_name, player2_name):
    """
    Realiza la tirada de dados inicial para decidir quién empieza.
    Muestra una mini interfaz con los resultados y maneja los empates.
    Devuelve el índice del jugador que empieza (0 o 1).
    """
    print("\n--- Tirada para decidir quién empieza ---")
    while True:
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)

        print(f"{player1_name} (blancas) ha sacado un: {d1}")
        print(f"{player2_name} (negras) ha sacado un: {d2}")

        if d1 > d2:
            print(f"¡{player1_name} empieza!")
            return 0
        if d2 > d1:
            print(f"¡{player2_name} empieza!")
            return 1
        else:
            print("¡Empate! Volvemos a tirar los dados.")
            input("Presiona Enter para tirar de nuevo...")


def _display_possible_moves(moves):
    """
    Muestra la lista de movimientos posibles, ajustando la numeración
    interna (0-23) a la mostrada al usuario (1-24).
    """
    if not moves:
        return

    print("Movimientos posibles:")
    for i, move in enumerate(moves, 1):
        if move.startswith("sacar"):
            # El formato "sacar [número]" ya es amigable para el usuario
            print(f"{i}) {move.capitalize()}")
        elif " a " in move:
            parts = move.split(" a ")
            from_str = parts[0]
            to_str = parts[1]

            display_move = ""
            if from_str == "Barra":
                # Reingreso desde la barra
                to_pos = int(to_str) + 1
                display_move = f"Barra a {to_pos}"
            else:
                # Movimiento normal
                from_pos = int(from_str) + 1
                display_to = str(int(to_str) + 1)
                display_move = f"{from_pos} a {display_to}"

            print(f"{i}) {display_move}")


def main():
    """
    La función principal para el juego de Backgammon en CLI.
    """
    print("¡Bienvenido a Backgammon CLI!")

    # 1. Obtener nombres de los jugadores
    player1_name, player2_name = _get_player_names()

    # 2. Decidir quién empieza
    first_player_idx = _decide_first_player(player1_name, player2_name)

    input("\nPresiona Enter para comenzar el juego...")

    # 3. Crear instancias del juego
    __board__ = Board()
    __dice__ = Dice()
    __player1__ = Player(player1_name, "white")
    __player2__ = Player(player2_name, "black")

    __game__ = Game(
        player1=__player1__, player2=__player2__, board=__board__, dice=__dice__
    )

    # 4. Establecer el jugador inicial y empezar el juego
    __game__.__current_turn__ = first_player_idx
    __game__.start()
    print(
        "Los jugadores se turnan para ingresar movimientos en el formato: 'desde hasta'"
    )
    print("Para retirar fichas, usa el comando: 'sacar [número]', ej. 'sacar 24'.")
    print("Escribe 'salir' para terminar.")

    while not __game__.is_over():
        print("\n" + "=" * 50)
        __current_player__ = __game__.get_current_player()
        print(
            f"Turno de {__current_player__.get_player_name()} "
            f"({'B' if __current_player__.__color__ == 'white' else 'N'})."
        )
        print(f"Tirada de dados: {__game__.get_dice_values()}")

        __game__.display_board()

        __possible_moves__ = __game__.get_possible_moves()
        if not __possible_moves__:
            print("No tienes movimientos posibles. El turno pasa al siguiente jugador.")
            __game__.switch_turn()
            continue

        _display_possible_moves(__possible_moves__)

        if not __game__.get_dice_values():
            continue

        # Mensaje contextual para bear-off
        if __game__.can_current_player_bear_off():
            print("Recuerda: para retirar una ficha, escribe 'sacar [número]'.")

        __move__ = input("Ingresa tu movimiento: ").strip().lower()
        if __move__ == "salir":
            print("Juego terminado.")
            break

        try:
            if __move__.startswith("sacar "):
                parts = __move__.split()
                if len(parts) == 2 and parts[1].isdigit():
                    from_pos = int(parts[1])
                    player_color = __game__.get_current_player().__color__
                    to_pos_bear_off = 24 if player_color == "white" else -1

                    if __game__.make_move(from_pos - 1, to_pos_bear_off):
                        print("Ficha retirada con éxito.")
                    else:
                        print("Movimiento de 'sacar' inválido.")
                else:
                    print("Formato de 'sacar' inválido. Usa 'sacar [número]'.")
                continue

            # Procesar reingreso (un solo número)
            if __game__.current_player_has_captured() and __move__.isdigit():
                to_pos = int(__move__) - 1
                if __game__.make_move(-1, to_pos):  # -1 indica "desde la barra"
                    print("Movimiento exitoso.")
                else:
                    print("Movimiento de reingreso inválido.")
                continue

            # Procesar movimiento normal 'desde hasta'
            if " " in __move__:
                __from_pos__, __to_pos__ = map(int, __move__.split())
                if __game__.make_move(__from_pos__ - 1, __to_pos__ - 1):
                    print("Movimiento exitoso.")
                else:
                    print("Movimiento inválido.")
                continue

            print("Formato de entrada no reconocido. Inténtalo de nuevo.")

        except (ValueError, IndexError):
            print("Entrada inválida. Asegúrate de usar el formato correcto.")

    if __game__.is_over():
        __winner__ = __game__.get_winner()
        if __winner__:
            print(f"\n¡Juego terminado! ¡{__winner__.get_player_name()} gana!")
        else:
            print("\n¡Juego terminado!")


if __name__ == "__main__":
    main()
