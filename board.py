from pieces import *

class Board:

    def __init__(self):

        self.board = [

            [-4,-2,-3,-5,-6,-3,-2,-4],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [4,2,3,5,6,3,2,4]

        ]

        self.white_to_move = True

        self.white_can_castle_kingside = True
        self.white_can_castle_queenside = True
        self.black_can_castle_kingside = True
        self.black_can_castle_queenside = True
        self.en_passant_target = None


    def print_board(self):

        for row in self.board:
            print(row)

        print()

    def make_move(self, move):

        old_castling_rights = (
            self.white_can_castle_kingside,
            self.white_can_castle_queenside,
            self.black_can_castle_kingside,
            self.black_can_castle_queenside
        )

        old_en_passant_target = self.en_passant_target

        if len(move) == 5:
            r1, c1, r2, c2, special = move
        else:
            r1, c1, r2, c2 = move
            special = None

        piece = self.board[r1][c1]
        captured = self.board[r2][c2]

        self.board[r1][c1] = EMPTY
        self.en_passant_target = None

        if special == "promotion":
            if piece > 0:
                self.board[r2][c2] = WHITE_QUEEN
            else:
                self.board[r2][c2] = BLACK_QUEEN

        elif special == "castle_kingside":
            self.board[r2][c2] = piece
            self.board[r2][5] = self.board[r2][7]
            self.board[r2][7] = EMPTY

        elif special == "castle_queenside":
            self.board[r2][c2] = piece
            self.board[r2][3] = self.board[r2][0]
            self.board[r2][0] = EMPTY

        elif special == "en_passant":
            self.board[r2][c2] = piece
            if piece > 0:
                captured = self.board[r2 + 1][c2]
                self.board[r2 + 1][c2] = EMPTY
            else:
                captured = self.board[r2 - 1][c2]
                self.board[r2 - 1][c2] = EMPTY

        else:
            self.board[r2][c2] = piece

        # set en passant target after a double pawn move
        if abs(piece) == 1 and abs(r2 - r1) == 2:
            self.en_passant_target = ((r1 + r2) // 2, c1)

        # update castling rights if king moves
        if piece == WHITE_KING:
            self.white_can_castle_kingside = False
            self.white_can_castle_queenside = False
        elif piece == BLACK_KING:
            self.black_can_castle_kingside = False
            self.black_can_castle_queenside = False

        # update castling rights if rook moves
        elif piece == WHITE_ROOK:
            if r1 == 7 and c1 == 0:
                self.white_can_castle_queenside = False
            elif r1 == 7 and c1 == 7:
                self.white_can_castle_kingside = False

        elif piece == BLACK_ROOK:
            if r1 == 0 and c1 == 0:
                self.black_can_castle_queenside = False
            elif r1 == 0 and c1 == 7:
                self.black_can_castle_kingside = False

        # update castling rights if rook is captured
        if captured == WHITE_ROOK:
            if r2 == 7 and c2 == 0:
                self.white_can_castle_queenside = False
            elif r2 == 7 and c2 == 7:
                self.white_can_castle_kingside = False

        elif captured == BLACK_ROOK:
            if r2 == 0 and c2 == 0:
                self.black_can_castle_queenside = False
            elif r2 == 0 and c2 == 7:
                self.black_can_castle_kingside = False

        self.white_to_move = not self.white_to_move

        return captured, old_castling_rights, old_en_passant_target


    def undo_move(self, move, move_state):

        captured, old_castling_rights, old_en_passant_target = move_state

        self.white_can_castle_kingside, self.white_can_castle_queenside, \
        self.black_can_castle_kingside, self.black_can_castle_queenside = old_castling_rights

        self.en_passant_target = old_en_passant_target

        if len(move) == 5:
            r1, c1, r2, c2, special = move
        else:
            r1, c1, r2, c2 = move
            special = None

        piece = self.board[r2][c2]

        if special == "promotion":
            piece = WHITE_PAWN if piece > 0 else BLACK_PAWN
            self.board[r1][c1] = piece
            self.board[r2][c2] = captured

        elif special == "castle_kingside":
            self.board[r1][c1] = piece
            self.board[r2][c2] = EMPTY
            self.board[r2][7] = self.board[r2][5]
            self.board[r2][5] = EMPTY

        elif special == "castle_queenside":
            self.board[r1][c1] = piece
            self.board[r2][c2] = EMPTY
            self.board[r2][0] = self.board[r2][3]
            self.board[r2][3] = EMPTY

        elif special == "en_passant":
            self.board[r1][c1] = piece
            self.board[r2][c2] = EMPTY

            if piece > 0:
                self.board[r2 + 1][c2] = BLACK_PAWN
            else:
                self.board[r2 - 1][c2] = WHITE_PAWN

        else:
            self.board[r1][c1] = piece
            self.board[r2][c2] = captured

        self.white_to_move = not self.white_to_move


    def square_is_attacked(self, row, col, by_white):
        # 1. pawn attacks
        if by_white:
            pawn_attack_row = row + 1
            for dc in [-1, 1]:
                pc = col + dc
                if 0 <= pawn_attack_row < 8 and 0 <= pc < 8:
                    if self.board[pawn_attack_row][pc] == WHITE_PAWN:
                        return True
        else:
            pawn_attack_row = row - 1
            for dc in [-1, 1]:
                pc = col + dc
                if 0 <= pawn_attack_row < 8 and 0 <= pc < 8:
                    if self.board[pawn_attack_row][pc] == BLACK_PAWN:
                        return True

        # 2. knight attacks
        knight_offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        attacker_knight = WHITE_KNIGHT if by_white else BLACK_KNIGHT

        for dr, dc in knight_offsets:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == attacker_knight:
                    return True

        # 3. bishop / queen diagonal attacks
        diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        attacker_bishop = WHITE_BISHOP if by_white else BLACK_BISHOP
        attacker_queen = WHITE_QUEEN if by_white else BLACK_QUEEN

        for dr, dc in diagonal_dirs:
            nr = row + dr
            nc = col + dc

            while 0 <= nr < 8 and 0 <= nc < 8:
                piece = self.board[nr][nc]

                if piece != EMPTY:
                    if piece == attacker_bishop or piece == attacker_queen:
                        return True
                    break

                nr += dr
                nc += dc

        # 4. rook / queen straight attacks
        straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        attacker_rook = WHITE_ROOK if by_white else BLACK_ROOK

        for dr, dc in straight_dirs:
            nr = row + dr
            nc = col + dc

            while 0 <= nr < 8 and 0 <= nc < 8:
                piece = self.board[nr][nc]

                if piece != EMPTY:
                    if piece == attacker_rook or piece == attacker_queen:
                        return True
                    break

                nr += dr
                nc += dc

        # 5. king attacks
        attacker_king = WHITE_KING if by_white else BLACK_KING
        king_dirs = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in king_dirs:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == attacker_king:
                    return True

        return False
    

    def find_king(self, white):
        target = WHITE_KING if white else BLACK_KING

        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)

        return None


    def is_in_check(self, white):
        king_pos = self.find_king(white)

        if king_pos is None:
            return False

        kr, kc = king_pos
        return self.square_is_attacked(kr, kc, not white)
    
    
    def print_pretty(self):
        piece_to_symbol = {
            0: ".",
            WHITE_PAWN: "P",
            WHITE_KNIGHT: "N",
            WHITE_BISHOP: "B",
            WHITE_ROOK: "R",
            WHITE_QUEEN: "Q",
            WHITE_KING: "K",
            BLACK_PAWN: "p",
            BLACK_KNIGHT: "n",
            BLACK_BISHOP: "b",
            BLACK_ROOK: "r",
            BLACK_QUEEN: "q",
            BLACK_KING: "k"
        }

        print("  a b c d e f g h")
        for r in range(8):
            rank = 8 - r
            row_str = str(rank) + " "
            for c in range(8):
                row_str += piece_to_symbol[self.board[r][c]] + " "
            print(row_str)
        print()

    def is_checkmate(self):
        from move_generator import MoveGenerator
        generator = MoveGenerator(self)
        moves = generator.generate_moves()
        return len(moves) == 0 and self.is_in_check(self.white_to_move)

    def is_stalemate(self):
        from move_generator import MoveGenerator
        generator = MoveGenerator(self)
        moves = generator.generate_moves()
        return len(moves) == 0 and not self.is_in_check(self.white_to_move)
    
    
    
    

    