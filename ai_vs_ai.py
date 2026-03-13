from board import Board
from search import find_best_move
from utils import move_to_text

def main():
    board = Board()

    max_turns = 900

    for turn in range(max_turns):
        print(f"Turn {turn + 1}")
        board.print_pretty()

        if board.is_checkmate():
            winner = "Black" if board.white_to_move else "White"
            print("Checkmate!")
            print("Winner:", winner)
            return

        if board.is_stalemate():
            print("Stalemate!")
            return

        move = find_best_move(board, 3)

        if move is None:
            print("No legal move found.")
            return

        side = "White" if board.white_to_move else "Black"
        print(side, "plays:", move_to_text(move))

        board.make_move(move)

    print("Reached move limit.")
    board.print_pretty()

if __name__ == "__main__":
    main()