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
        print("\n" + "="*50)
        __current_player__ = __game__.get_current_player()
        print(f"Turno de {__current_player__.get_name()} ({'O' if __current_player__.__color__ == 'white' else 'X'}).")
        print(f"Tirada de dados: {__game__.get_dice_values()}")
        
        __game__.display_board()

        __possible_moves__ = __game__.get_possible_moves()
        if not __possible_moves__:
            print("No tienes movimientos posibles. El turno pasa al siguiente jugador.")
            __game__.switch_turn()
            continue

        print("Movimientos posibles:", ", ".join(__possible_moves__))

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
