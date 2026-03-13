from board import Board
from search import find_best_move
from move_generator import MoveGenerator
from utils import move_to_text, text_to_move

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False
        print("Please answer with yes/no or y/n.")

def main():
    board = Board()

    human_is_white = ask_yes_no("Do you want to play as White? (y/n): ")
    show_legal_moves = ask_yes_no("Do you want to display all legal moves each turn? (y/n): ")
    search_depth = 3

    while True:
        board.print_pretty()

        if board.is_checkmate():
            winner = "Black" if board.white_to_move else "White"
            print("Checkmate!")
            print("Winner:", winner)
            break

        if board.is_stalemate():
            print("Stalemate!")
            break

        if board.white_to_move == human_is_white:
            print("Your turn.")
            generator = MoveGenerator(board)
            legal_moves = generator.generate_moves()

            if show_legal_moves:
                print("Legal moves:")
                for move in legal_moves:
                    print(move_to_text(move))

            user_input = input("Enter your move (example: e2e4): ")
            move = text_to_move(user_input, legal_moves)

            if move is None:
                print("Invalid move. Try again.")
                continue

            print("You played:", move_to_text(move))
            board.make_move(move)

        else:
            print("AI thinking...")
            move = find_best_move(board, search_depth)

            if move is None:
                print("AI has no legal moves.")
                break

            print("AI plays:", move_to_text(move))
            board.make_move(move)

if __name__ == "__main__":
    main()