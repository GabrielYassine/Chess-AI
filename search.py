from evaluation import evaluate
from move_generator import MoveGenerator
from pieces import *
from config import CHECKMATE_SCORE, STALEMATE_SCORE

nodes_searched = 0


def move_ordering_score(board, move):
    score = 0

    if len(move) == 5:
        _, _, r2, c2, special = move
    else:
        _, _, r2, c2 = move
        special = None

    target = board.board[r2][c2]

    if target != EMPTY:
        score += 1000 + abs(target)

    if special == "promotion":
        score += 2000

    if special == "castle_kingside" or special == "castle_queenside":
        score += 300

    if special == "en_passant":
        score += 900

    return score


def order_moves(board, moves):
    return sorted(moves, key=lambda move: move_ordering_score(board, move), reverse=True)


def alphabeta(board, depth, alpha, beta, maximizing_player):
    global nodes_searched
    nodes_searched += 1

    generator = MoveGenerator(board)
    moves = generator.generate_moves()

    if len(moves) == 0:
        if board.is_in_check(board.white_to_move):
            if maximizing_player:
                return -CHECKMATE_SCORE
            else:
                return CHECKMATE_SCORE
        else:
            return STALEMATE_SCORE

    if depth == 0:
        return evaluate(board)

    moves = order_moves(board, moves)

    if maximizing_player:
        max_eval = -999999999

        for move in moves:
            move_state = board.make_move(move)
            eval_score = alphabeta(board, depth - 1, alpha, beta, False)
            board.undo_move(move, move_state)

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, max_eval)

            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = 999999999

        for move in moves:
            move_state = board.make_move(move)
            eval_score = alphabeta(board, depth - 1, alpha, beta, True)
            board.undo_move(move, move_state)

            min_eval = min(min_eval, eval_score)
            beta = min(beta, min_eval)

            if beta <= alpha:
                break

        return min_eval


def find_best_move_at_depth(board, depth):
    generator = MoveGenerator(board)
    moves = generator.generate_moves()

    if len(moves) == 0:
        return None, None

    moves = order_moves(board, moves)

    best_move = None

    if board.white_to_move:
        best_value = -999999999

        for move in moves:
            move_state = board.make_move(move)
            value = alphabeta(board, depth - 1, -1000000000, 1000000000, False)
            board.undo_move(move, move_state)

            if value > best_value:
                best_value = value
                best_move = move
    else:
        best_value = 999999999

        for move in moves:
            move_state = board.make_move(move)
            value = alphabeta(board, depth - 1, -1000000000, 1000000000, True)
            board.undo_move(move, move_state)

            if value < best_value:
                best_value = value
                best_move = move

    return best_move, best_value


def find_best_move(board, max_depth):
    global nodes_searched

    best_move = None
    best_value = None

    for depth in range(1, max_depth + 1):
        nodes_searched = 0

        move, value = find_best_move_at_depth(board, depth)

        if move is not None:
            best_move = move
            best_value = value

        print(f"Depth {depth}: best move = {best_move}, eval = {best_value}, nodes = {nodes_searched}")

    return best_move