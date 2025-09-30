from core.game import Game  # Assuming Game class exists in game.py
from core.player import Player  # Assuming Player class exists in player.py


def main():
    # Initialize game and players
    player1 = Player("Player 1", __color__="white")
    player2 = Player("Player 2", __color__="black")
    game = Game(player1, player2)

    print("Welcome to Backgammon CLI!")
    print(
        "Players take turns entering moves in the format: 'from_position to_position'"
    )
    print("Type 'quit' to exit.")

    while not game.is_over():
        current_player = game.get_current_player()
        print(f"\n{current_player.name}'s turn.")
        game.display_board()  # Assuming Game has a display_board method

        move = input("Enter your move: ").strip()
        if move.lower() == "quit":
            print("Game exited.")
            break

        try:
            # Parse move, e.g., "1 4" for from 1 to 4
            from_pos, to_pos = map(int, move.split())
            if game.make_move(current_player, from_pos, to_pos):
                print("Move successful.")
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input format. Use 'from_position to_position'.")

    if game.is_over():
        winner = game.get_winner()
        print(f"\nGame over! {winner.name} wins!")


if __name__ == "__main__":
    main()
