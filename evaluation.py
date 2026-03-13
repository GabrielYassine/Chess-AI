from pieces import *
from move_generator import MoveGenerator

piece_values = {
    WHITE_PAWN: 100,
    WHITE_KNIGHT: 320,
    WHITE_BISHOP: 330,
    WHITE_ROOK: 500,
    WHITE_QUEEN: 900,
    WHITE_KING: 0,

    BLACK_PAWN: -100,
    BLACK_KNIGHT: -320,
    BLACK_BISHOP: -330,
    BLACK_ROOK: -500,
    BLACK_QUEEN: -900,
    BLACK_KING: 0
}

pawn_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, -2, -2, 0, 0, 0],
    [1, -1, -2, 0, 0, -2, -1, 1],
    [1, 2, 2, -2, -2, 2, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_table = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

bishop_table = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

rook_table = [
    [0, 0, 0, 0.5, 0.5, 0, 0, 0],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

queen_table = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
]

king_table = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]
]

def table_value(table, r, c, is_white):
    if is_white:
        return table[r][c]
    return table[7 - r][c]

def evaluate_material_and_position(board):
    score = 0

    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]

            if piece == EMPTY:
                continue

            score += piece_values[piece]

            if piece == WHITE_PAWN:
                score += pawn_table[r][c]
            elif piece == BLACK_PAWN:
                score -= table_value(pawn_table, r, c, False)

            elif piece == WHITE_KNIGHT:
                score += knight_table[r][c]
            elif piece == BLACK_KNIGHT:
                score -= table_value(knight_table, r, c, False)

            elif piece == WHITE_BISHOP:
                score += bishop_table[r][c]
            elif piece == BLACK_BISHOP:
                score -= table_value(bishop_table, r, c, False)

            elif piece == WHITE_ROOK:
                score += rook_table[r][c]
            elif piece == BLACK_ROOK:
                score -= table_value(rook_table, r, c, False)

            elif piece == WHITE_QUEEN:
                score += queen_table[r][c]
            elif piece == BLACK_QUEEN:
                score -= table_value(queen_table, r, c, False)

            elif piece == WHITE_KING:
                score += king_table[r][c]
            elif piece == BLACK_KING:
                score -= table_value(king_table, r, c, False)

    return score

def evaluate(board):
    score = evaluate_material_and_position(board)

    original_turn = board.white_to_move

    board.white_to_move = True
    white_moves = len(MoveGenerator(board).generate_moves())

    board.white_to_move = False
    black_moves = len(MoveGenerator(board).generate_moves())

    board.white_to_move = original_turn

    mobility_weight = 2
    score += mobility_weight * (white_moves - black_moves)

    return score