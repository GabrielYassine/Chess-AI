from search import find_best_move

def get_engine_move(board, depth=2):

    move = find_best_move(board, depth)

    return move