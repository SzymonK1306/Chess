import itertools
from PyQt5.QtWidgets import QMessageBox

import numpy as np


class ChessLogic:
    def __init__(self):
        # creating array to logic
        self.board_logic_array = np.array([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                                           ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                                           ['.', '.', '.', '.', '.', '.', '.', '.'],
                                           ['.', '.', '.', '.', '.', '.', '.', '.'],
                                           ['.', '.', '.', '.', '.', '.', '.', '.'],
                                           ['.', '.', '.', '.', '.', '.', '.', '.'],
                                           ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                                           ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])

        # color of active player
        self.color = 1
        self.check_now = False

        # castling flags
        self.white_king_moved = False
        self.white_right_rook = False
        self.white_left_rook = False

        self.black_king_moved = False
        self.black_right_rook = False
        self.black_left_rook = False

        # flags for highlight move
        self.white_right_castling_available = False
        self.white_left_castling_available = False

        self.black_right_castling_available = False
        self.black_left_castling_available = False

        # flags for qt to made move in GUI
        self.white_right_castling_done = False
        self.white_left_castling_done = False

        self.black_right_castling_done = False
        self.black_left_castling_done = False

        self.en_passant_target = None

        self.was_en_passant = True

        self.white_promotion = []
        self.black_promotion = []

        self.history_list = []
        self.column_array = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

    def move(self, startX, startY, stopX, stopY):
        """
        Make move on array board
        :param startX: int          :param startY: int        :param stopX: int        :param stopY: int
        :return:
        """
        self.was_en_passant = False

        piece = self.board_logic_array[startX, startY]
        self.board_logic_array[startX, startY] = '.'
        self.board_logic_array[stopX, stopY] = piece

        start_col = self.column_array[startY]
        start_row = str(8 - startX)

        stop_col = self.column_array[stopY]
        stop_row = str(8 - stopX)

        self.history_list.append(start_col + start_row + '-' + stop_col + stop_row)

        # set castling flags
        if piece == 'K':
            self.white_king_moved = True
        if piece == 'k':
            self.black_king_moved = True
        if piece == 'R' and startY == 7:
            self.white_right_rook = True
        if piece == 'R' and startY == 0:
            self.white_left_rook = True
        if piece == 'r' and startY == 7:
            self.black_right_rook = True
        if piece == 'r' and startY == 0:
            self.black_left_rook = True

        # castling realisation on
        if piece == 'K' or piece == 'k':
            self.castling_check(stopY)

        if self.en_passant_target is not None:
            rowEn, colEn = self.en_passant_target
            if (piece == 'P' and self.board_logic_array[rowEn, colEn] == 'p') or piece == 'p' and self.board_logic_array[rowEn, colEn] == 'P':
                if (stopX + (1 if piece.isupper() else -1), stopY) == self.en_passant_target:
                    self.board_logic_array[rowEn, colEn] = '.'
                    self.was_en_passant = True

        # if piece == 'P' or piece == 'p':
        #     if self.en_passant_target is not None:
        #         if self.en_passant_target[1] == stopY:
        #             if abs(self.en_passant_target[0] - stopX) == 1:
        #                 self.was_en_passant = True
        #                 if piece.isupper():
        #                     self.board_logic_array[self.en_passant_target[0] + 1, self.en_passant_target[1]] = '.'
        #                 else:
        #                     self.board_logic_array[self.en_passant_target[0] - 1, self.en_passant_target[1]] = '.'


        # en passant
        self.en_passant_target = None

        # when pawn make double first move
        if piece == 'P' or piece == 'p':
            if abs(stopX - startX) > 1:
                self.en_passant_target = (stopX, stopY)

        white_promotion = np.where(self.board_logic_array[0] == 'P')
        black_promotion = np.where(self.board_logic_array[7] == 'p')

        if len(white_promotion[0]) != 0:
            self.white_promotion = [white_promotion[0]]
        if len(black_promotion[0]) != 0:
            self.black_promotion = [black_promotion[0]]
        # change color alter move
        # white - 1, black - 0
        if self.color:
            self.color = 0
        else:
            self.color = 1

        self.check_now, _ = self.is_check()
        if self.check_now:
            checkmate = not any(self.get_piece_moves(x, y)
                                for x, y in itertools.product(range(8), range(8))
                                if self.board_logic_array[x, y] != '.'
                                and self.board_logic_array[x, y].isupper() == self.color)
            if checkmate:
                color_text = 'Black' if self.color else 'White'
                message_box = QMessageBox()
                message_box.setWindowTitle('Checkmate!')
                message_box.setText("Checkmate! Game over. " + color_text + ' wins')
                message_box.exec()

        print(self.board_logic_array)


    def get_piece_moves(self, row, col):
        """
        Get possible move of piece in given position
        :param row: int        :param col: int
        :return: list
        """
        moves = []
        piece = self.board_logic_array[row, col]

        # all possible moves for the piece
        moves = self.single_piece_move(piece, row, col)

        # delete move which will reveal king
        moves = self.check_legal_moves(moves, row, col)

        return moves

    def castling_check(self, stopY):
        # white right
        if self.white_right_castling_available and stopY == 6:
            self.board_logic_array[7, 7] = '.'
            self.board_logic_array[7, 5] = 'R'
            self.white_right_castling_done = True

            # white castling impossible
            self.white_right_castling_available = False
            self.white_left_castling_available = False

        # white left
        if self.white_left_castling_available and stopY == 2:
            self.board_logic_array[7, 0] = '.'
            self.board_logic_array[7, 3] = 'R'
            self.white_left_castling_done = True

            # white castling impossible
            self.white_right_castling_available = False
            self.white_left_castling_available = False
        # black right
        if self.black_right_castling_available and stopY == 6:
            self.board_logic_array[0, 7] = '.'
            self.board_logic_array[0, 5] = 'r'
            self.black_right_castling_done = True

            # black castling impossible
            self.black_right_castling_available = False
            self.black_left_castling_available = False

        # black left
        if self.black_left_castling_available and stopY == 2:
            self.board_logic_array[0, 0] = '.'
            self.board_logic_array[0, 3] = 'r'
            self.black_left_castling_done = True

            # black castling impossible
            self.black_right_castling_available = False
            self.black_left_castling_available = False

    def single_piece_move(self, piece,  row, col):
        """
        Get all possible moves, even if it reveals king
        :param piece: str
        :param row: int        :param col: int
        :return: list of tuples (moves)
        """
        if piece == 'P' or piece == 'p':
            moves = self.get_pawn_moves(row, col)
        elif piece == 'N' or piece == 'n':
            moves = self.get_knight_moves((row, col), piece.isupper())
        elif piece == 'B' or piece == 'b':
            moves = self.get_bishop_moves((row, col))
        elif piece == 'R' or piece == 'r':
            moves = self.get_rook_moves((row, col))
        elif piece == 'Q' or piece == 'q':
            moves = self.get_queen_moves((row, col))
        elif piece == 'K' or piece == 'k':
            moves = self.get_king_moves((row, col))

        return moves

    def get_pawn_moves(self, row, col):
        """
        :param row: int        :param col: int
        :return: list of pawn moves
        """

        moves = []
        piece = self.board_logic_array[row, col]

        # Check if the Pawn is white or black
        if piece.isupper():
            direction = -1  # White Pawns move up the board
            start_row = 6  # White Pawns start on row 6
        else:
            direction = 1  # Black Pawns move down the board
            start_row = 1  # Black Pawns start on row 1

        # Check the Pawn's first move
        if row == start_row:
            # Pawn can move 1 or 2 squares forward on its first move
            if self.board_logic_array[row + direction, col] == '.':
                moves.append((row + direction, col))
                if self.board_logic_array[row + 2 * direction, col] == '.':
                    moves.append((row + 2 * direction, col))

        # Check forward moves
        if row + direction >= 0 and row + direction <= 7:
            if self.board_logic_array[row + direction, col] == '.':
                moves.append((row + direction, col))

        # checking en passant
        if self.en_passant_target is not None:
            rowEn, colEn = self.en_passant_target
            if row == rowEn and (col - 1 == colEn or col + 1 == colEn):
                moves.append((rowEn + direction, colEn))
                # self.was_en_passant = True

        # Check diagonal capture moves (white)
        if direction == -1:
            if col > 0 and row + direction >= 0 and row + direction <= 7:
                if self.board_logic_array[row + direction, col - 1].islower():
                    moves.append((row + direction, col - 1))
            if col < 7 and row + direction >= 0 and row + direction <= 7:
                if self.board_logic_array[row + direction, col + 1].islower():
                    moves.append((row + direction, col + 1))

        # Check diagonal capture moves (black)
        if direction == 1:
            if col > 0 and row + direction >= 0 and row + direction <= 7:
                if self.board_logic_array[row + direction, col - 1].isupper():
                    moves.append((row + direction, col - 1))
            if col < 7 and row + direction >= 0 and row + direction <= 7:
                if self.board_logic_array[row + direction, col + 1].isupper():
                    moves.append((row + direction, col + 1))

        return moves

    def get_knight_moves(self, pos, color):
        """
        Given a chess board, a position of a knight, and the color of the knight,
        returns all possible moves for that knight.
        """
        row, col = pos

        moves = [(new_row, new_col) for dr, dc in
                 [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
                 for new_row, new_col in [(row + dr, col + dc)]
                 if 0 <= new_row < 8 and 0 <= new_col < 8 and (self.board_logic_array[new_row][new_col] == '.' or (
                        self.board_logic_array[new_row][new_col].isupper() ^ color))]

        return moves

    def get_bishop_moves(self, current_pos):
        x, y = current_pos

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Check all 4 diagonal directions
        bishop_moves = [move for dir in directions for move in self.avoid_loop_bishop(self.board_logic_array[x, y], x, y, dir[0], dir[1])]

        return bishop_moves

    def avoid_loop_bishop(self, piece, x, y, dx, dy):
        validPos = [(x + i * dx, y + i * dy)
                    for i in range(1, 8)
                    if 0 <= x + i * dx < 8 and 0 <= y + i * dy < 8 and (self.board_logic_array[x + i * dx, y + i * dy] == '.'
                    or self.board_logic_array[x + i * dx, y + i * dy].isupper() != piece.isupper())
                    and not any(self.board_logic_array[x + j * dx, y + j * dy] != '.' for j in range(1, i))]

        return validPos

    def get_rook_moves(self, current_pos):
        x, y = current_pos
        rook_directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        rook_moves = [move for dir in rook_directions for move in self.avoid_loop_rook(self.board_logic_array[x, y], x, y, dir[0], dir[1])]

        return rook_moves

    def avoid_loop_rook(self, piece, x, y, dir_x, dir_y):
        line_array = np.array([(i * dir_x + x, i * dir_y + y) for i in range(1, 8)])
        valid_ind = np.all((line_array >= 0) & (line_array < 8), axis=1)
        valid_pos = line_array[valid_ind]

        target_pieces = [self.board_logic_array[pos[0], pos[1]] for pos in valid_pos]
        first_non_empty = next((i for i, p in enumerate(target_pieces) if p != '.'), len(target_pieces))

        if first_non_empty < len(target_pieces) and target_pieces[first_non_empty].isupper() != piece.isupper():
            return [(x[0], x[1]) for x in valid_pos[:first_non_empty + 1].tolist()]
        else:
            return [(x[0], x[1]) for x in valid_pos[:first_non_empty].tolist()]

    def get_queen_moves(self, current_pos):
        queen_moves = self.get_bishop_moves(current_pos) + self.get_rook_moves(current_pos)
        return queen_moves

    def get_king_moves(self, current_pos):
        row, col = current_pos
        # Get the color of the king
        color = self.board_logic_array[row, col].isupper()

        # Define the list of all possible moves for the king
        moves = [(row + i, col + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]

        # Filter out any moves that are not valid
        valid_moves = [(r, c) for r, c in moves if 0 <= r < 8 and 0 <= c < 8 and (self.board_logic_array[r, c] == '.'
                                                                                  or self.board_logic_array[r, c].isupper() != color)]
        return valid_moves

    def check_legal_moves(self, moves, row, col):
        """
        Delete illegal moves
        :param moves: list of tuples
        :param row: int        :param col: int
        :return: list of tuples
        """
        legal_moves = []

        # make a copy of board
        self.board_backup = np.copy(self.board_logic_array)

        # check move
        legal_moves = [self.move_checking(row, col, move[0], move[1]) for move in moves if self.move_checking(row, col, move[0], move[1]) is not None]

        self.board_logic_array = np.copy(self.board_backup)

        # Check castling is possible
        # white
        if self.color and row == 7 and col == 4:    # white and king is chosen
            if not self.white_king_moved:
                # right castling check
                if not self.white_right_rook and self.board_logic_array[7, 6] == '.' and self.board_logic_array[7, 5] == '.':
                    if not self.is_square_under_attack((7, 6)) and not self.is_square_under_attack((7, 5)) and not self.is_square_under_attack((7, 4)):
                        legal_moves.append((7, 6))
                        self.white_right_castling_available = True
                # left castling check
                if not self.white_left_rook and self.board_logic_array[7, 3] == '.' and self.board_logic_array[7, 2] == '.' and self.board_logic_array[7, 1] == '.':
                    if not self.is_square_under_attack((7, 3)) and not self.is_square_under_attack((7, 2)) and not self.is_square_under_attack((7, 4)):
                        legal_moves.append((7, 2))
                        self.white_left_castling_available = True

        # black
        if not self.color and row == 0 and col == 4:    # black and king is chosen
            if not self.black_king_moved:
                # right castling check
                if not self.black_right_rook and self.board_logic_array[0, 6] == '.' and self.board_logic_array[0, 5] == '.':
                    if not self.is_square_under_attack((0, 6)) and not self.is_square_under_attack((0, 5)) and not self.is_square_under_attack((0, 4)):
                        legal_moves.append((0, 6))
                        self.black_right_castling_available = True
                # left castling check
                if not self.black_left_rook and self.board_logic_array[0, 3] == '.' and self.board_logic_array[0, 2] == '.' and self.board_logic_array[0, 1] == '.':
                    if not self.is_square_under_attack((0, 3)) and not self.is_square_under_attack((0, 2)) and not self.is_square_under_attack((0, 4)):
                        legal_moves.append((0, 2))
                        self.black_left_castling_available = True

        return legal_moves

    def move_checking(self, row, col, start, stop):
        legal = False

        # make test move
        self.test_move(row, col, start, stop)

        # if there is no check, it is legal
        if not self.is_in_check():
            legal = True

        # restore original board
        self.board_logic_array = np.copy(self.board_backup)

        if legal:
            return (start, stop)
        else:
            return None

    def is_square_under_attack(self, position):
        """
        Check that someone can attack given field
        :param position: tuple
        :return: bool
        """
        # color white - 1 black - 0
        for x, y in itertools.product(range(8), range(8)):
            piece = self.board_logic_array[x][y]

            if piece != '.' and piece.isupper() != self.color:
                moves = self.single_piece_move(piece, x, y)

                if (position[0], position[1]) in moves:
                    return True
        return False

    def is_check(self):
        """
        Checking that active player made check
        :return:
        """
        if self.color:
            king_position = np.argwhere(self.board_logic_array == 'K')[0]
        else:
            king_position = np.argwhere(self.board_logic_array == 'k')[0]

        is_check = self.is_square_under_attack(king_position)
        king_position = [(king_position[0], king_position[1])]

        self.check_now = is_check

        return is_check, king_position

    def is_in_check(self):
        """
        Checking check on active player site, to detect forbidden move
        :return:
        """
        if self.color:
            king_position = np.argwhere(self.board_logic_array == 'K')[0]
        else:
            king_position = np.argwhere(self.board_logic_array == 'k')[0]

        is_in_check = self.is_square_under_attack(king_position)

        self.check_now = is_in_check

        return is_in_check

    def test_move(self, startX, startY, stopX, stopY):
        """
        Make test move to check legal moves
        :param startX: int        :param startY: int        :param stopX: int        :param stopY: int
        :return:
        """
        piece = self.board_logic_array[startX, startY]
        self.board_logic_array[startX, startY] = '.'
        self.board_logic_array[stopX, stopY] = piece

    def pawn_promotion(self, x, y, chosen_piece):
        pawn = self.board_logic_array[x][y]

        match chosen_piece:
            case 'Queen':
                if pawn.isupper():
                    self.board_logic_array[x][y] = 'Q'
                else:
                    self.board_logic_array[x][y] = 'q'
            case 'Rook':
                if pawn.isupper():
                    self.board_logic_array[x][y] = 'R'
                else:
                    self.board_logic_array[x][y] = 'r'
            case 'Bishop':
                if pawn.isupper():
                    self.board_logic_array[x][y] = 'B'
                else:
                    self.board_logic_array[x][y] = 'b'
            case 'Knight':
                if pawn.isupper():
                    self.board_logic_array[x][y] = 'N'
                else:
                    self.board_logic_array[x][y] = 'n'

