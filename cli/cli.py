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
        elif d2 > d1:
            print(f"¡{player2_name} empieza!")
            return 1
        else:
            print("¡Empate! Volvemos a tirar los dados.")
            input("Presiona Enter para tirar de nuevo...")


def _display_possible_moves(moves):
    """Muestra la lista de movimientos posibles en formato vertical."""
    if moves:
        print("Movimientos posibles:")
        for i, move in enumerate(moves, 1):
            print(f"{i}) {move}")


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
    print("Escribe 'salir' para terminar.")

    while not __game__.is_over():
        print("\n" + "=" * 50)
        __current_player__ = __game__.get_current_player()
        print(
            f"Turno de {__current_player__.get_name()} ({'O' if __current_player__.__color__ == 'white' else 'X'})."
        )
        print(f"Tirada de dados: {__game__.get_dice_values()}")

        __game__.display_board()

        __possible_moves__ = __game__.get_possible_moves()
        if not __possible_moves__:
            print("No tienes movimientos posibles. El turno pasa al siguiente jugador.")
            __game__.switch_turn()
            continue

        _display_possible_moves(__possible_moves__)

        # Si no quedan dados, el turno debería cambiar. make_move se encarga de esto.
        if not __game__.get_dice_values():
            # No es necesario cambiar de turno aquí, make_move lo gestiona
            continue

        __move__ = input("Ingresa tu movimiento ('desde hasta', ej. '18 23'): ").strip()
        if __move__.lower() == "salir":
            print("Juego terminado.")
            break

        try:
            __from_pos__, __to_pos__ = map(int, __move__.split())
            if __game__.make_move(__from_pos__, __to_pos__):
                print("Movimiento exitoso.")
            else:
                print("Movimiento inválido. Inténtalo de nuevo.")
        except ValueError:
            print("Formato de entrada inválido. Usa 'desde hasta'.")
        except IndexError as e:
            print(f"Error: {e}")

    if __game__.is_over():
        __winner__ = __game__.get_winner()
        if __winner__:
            print(f"\n¡Juego terminado! ¡{__winner__.get_name()} gana!")
        else:
            print("\n¡Juego terminado!")


if __name__ == "__main__":
    main()
