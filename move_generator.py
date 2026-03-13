from pieces import *

class MoveGenerator:

    def __init__(self, board):
        self.board = board

    def generate_pseudo_legal_moves(self):
        moves = []

        for r in range(8):
            for c in range(8):
                piece = self.board.board[r][c]

                if piece == EMPTY:
                    continue

                if self.board.white_to_move and piece > 0:
                    moves.extend(self.generate_piece_moves(r, c, piece))
                elif not self.board.white_to_move and piece < 0:
                    moves.extend(self.generate_piece_moves(r, c, piece))

        return moves

    def generate_moves(self):
        pseudo_moves = self.generate_pseudo_legal_moves()
        legal_moves = []

        side_to_move = self.board.white_to_move

        for move in pseudo_moves:
            move_state = self.board.make_move(move)

            if not self.board.is_in_check(side_to_move):
                legal_moves.append(move)

            self.board.undo_move(move, move_state)

        return legal_moves

    def generate_piece_moves(self, r, c, piece):
        moves = []

        if abs(piece) == 1:
            moves.extend(self.pawn_moves(r, c, piece))
        elif abs(piece) == 2:
            moves.extend(self.knight_moves(r, c, piece))
        elif abs(piece) == 3:
            moves.extend(self.bishop_moves(r, c, piece))
        elif abs(piece) == 4:
            moves.extend(self.rook_moves(r, c, piece))
        elif abs(piece) == 5:
            moves.extend(self.queen_moves(r, c, piece))
        elif abs(piece) == 6:
            moves.extend(self.king_moves(r, c, piece))
            moves.extend(self.castling_moves(r, c, piece))

        return moves

    def pawn_moves(self, r, c, piece):
        moves = []

        direction = -1 if piece > 0 else 1
        start_row = 6 if piece > 0 else 1
        promotion_row = 0 if piece > 0 else 7

        nr = r + direction

        if 0 <= nr < 8 and self.board.board[nr][c] == EMPTY:
            if nr == promotion_row:
                moves.append((r, c, nr, c, "promotion"))
            else:
                moves.append((r, c, nr, c))

            if r == start_row:
                nr2 = r + 2 * direction
                if 0 <= nr2 < 8 and self.board.board[nr2][c] == EMPTY:
                    moves.append((r, c, nr2, c))

        for dc in [-1, 1]:
            nc = c + dc
            nr = r + direction

            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]

                if target != EMPTY and target * piece < 0:
                    if nr == promotion_row:
                        moves.append((r, c, nr, nc, "promotion"))
                    else:
                        moves.append((r, c, nr, nc))

        # en passant
        if self.board.en_passant_target is not None:
            ep_r, ep_c = self.board.en_passant_target
            if nr == ep_r and abs(c - ep_c) == 1:
                moves.append((r, c, ep_r, ep_c, "en_passant"))

        return moves

    def knight_moves(self, r, c, piece):
        moves = []

        knight_offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for dr, dc in knight_offsets:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]

                if target == EMPTY or target * piece < 0:
                    moves.append((r, c, nr, nc))

        return moves

    def bishop_moves(self, r, c, piece):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            while 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]

                if target == EMPTY:
                    moves.append((r, c, nr, nc))
                elif target * piece < 0:
                    moves.append((r, c, nr, nc))
                    break
                else:
                    break

                nr += dr
                nc += dc

        return moves

    def rook_moves(self, r, c, piece):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            while 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]

                if target == EMPTY:
                    moves.append((r, c, nr, nc))
                elif target * piece < 0:
                    moves.append((r, c, nr, nc))
                    break
                else:
                    break

                nr += dr
                nc += dc

        return moves

    def queen_moves(self, r, c, piece):
        moves = []
        moves.extend(self.bishop_moves(r, c, piece))
        moves.extend(self.rook_moves(r, c, piece))
        return moves

    def king_moves(self, r, c, piece):
        moves = []

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < 8 and 0 <= nc < 8:
                target = self.board.board[nr][nc]

                if target == EMPTY or target * piece < 0:
                    moves.append((r, c, nr, nc))

        return moves

    def castling_moves(self, r, c, piece):
        moves = []

        if self.board.is_in_check(piece > 0):
            return moves

        if piece == WHITE_KING and r == 7 and c == 4:
            if self.board.white_can_castle_kingside:
                if self.board.board[7][7] == WHITE_ROOK:
                    if self.board.board[7][5] == EMPTY and self.board.board[7][6] == EMPTY:
                        if not self.board.square_is_attacked(7, 5, False) and not self.board.square_is_attacked(7, 6, False):
                            moves.append((7, 4, 7, 6, "castle_kingside"))

            if self.board.white_can_castle_queenside:
                if self.board.board[7][0] == WHITE_ROOK:
                    if self.board.board[7][1] == EMPTY and self.board.board[7][2] == EMPTY and self.board.board[7][3] == EMPTY:
                        if not self.board.square_is_attacked(7, 3, False) and not self.board.square_is_attacked(7, 2, False):
                            moves.append((7, 4, 7, 2, "castle_queenside"))

        elif piece == BLACK_KING and r == 0 and c == 4:
            if self.board.black_can_castle_kingside:
                if self.board.board[0][7] == BLACK_ROOK:
                    if self.board.board[0][5] == EMPTY and self.board.board[0][6] == EMPTY:
                        if not self.board.square_is_attacked(0, 5, True) and not self.board.square_is_attacked(0, 6, True):
                            moves.append((0, 4, 0, 6, "castle_kingside"))

            if self.board.black_can_castle_queenside:
                if self.board.board[0][0] == BLACK_ROOK:
                    if self.board.board[0][1] == EMPTY and self.board.board[0][2] == EMPTY and self.board.board[0][3] == EMPTY:
                        if not self.board.square_is_attacked(0, 3, True) and not self.board.square_is_attacked(0, 2, True):
                            moves.append((0, 4, 0, 2, "castle_queenside"))

        return moves