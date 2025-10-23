"""
Módulo principal para la interfaz de línea de comandos del juego Backgammon.
"""
from core.game import Game
from core.player import Player


def main():
    """
    La función principal para el juego de Backgammon en CLI.
    """
    __player1__ = Player("Jugador 1", "white")
    __player2__ = Player("Jugador 2", "black")
    __game__ = Game(__player1__, __player2__)
    __game__.start()

    print("¡Bienvenido a Backgammon CLI!")
    print("Los jugadores se turnan para ingresar movimientos en el formato: 'desde hasta'")
    print("Escribe 'salir' para terminar.")

    while not __game__.is_over():
        __current_player__ = __game__.get_current_player()
        print(f"\nTurno de {__current_player__.get_name()}. Tirada de dados: {__game__.get_dice_values()}")
        __game__.display_board()

        if not __game__.get_dice_values():
            __game__.switch_turn()
            continue

        __move__ = input("Ingresa tu movimiento: ").strip()
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
