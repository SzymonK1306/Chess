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

        print(self.board_logic_array)

        # color of active player
        self.color = 1
        self.check_now = False

        self.white_promotion = []
        self.black_promotion = []

    def move(self, startX, startY, stopX, stopY):
        """
        Make move on array board
        :param startX: int          :param startY: int        :param stopX: int        :param stopY: int
        :return:
        """
        piece = self.board_logic_array[startX, startY]
        self.board_logic_array[startX, startY] = '.'
        self.board_logic_array[stopX, stopY] = piece

        white_promotion = np.where(self.board_logic_array[0] == 'P')
        black_promotion = np.where(self.board_logic_array[7] == 'p')
        print(self.board_logic_array[0])
        # print(white_promotion[0])
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
                message_box.setText("Checkmate! Game over. " + color_text + ' wins')
                message_box.exec()

        print(self.check_now)

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

        # Check if the piece is a Pawn
        if piece != 'P' and piece != 'p':
            print("Invalid selection: selected piece is not a Pawn.")
            return moves

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

        moves = []

        # Check all possible moves for the knight
        for dr, dc in [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            new_row, new_col = row + dr, col + dc

            # Check if the new position is on the board
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                # Check if the new position is not occupied by a piece of the same color
                if self.board_logic_array[new_row][new_col] == '.' or (self.board_logic_array[new_row][new_col].isupper() ^ color):
                    moves.append((new_row, new_col))

        return moves

    def get_bishop_moves(self, current_pos):
        x, y = current_pos
        bishop_moves = []
        color = self.board_logic_array[x][y].islower()

        # Check all 4 diagonal directions
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            i, j = x + dx, y + dy
            while 0 <= i < 8 and 0 <= j < 8:
                if self.board_logic_array[i][j] == '.':
                    bishop_moves.append((i, j))
                elif self.board_logic_array[i][j].islower() == color:
                    break
                else:
                    bishop_moves.append((i, j))
                    break
                i += dx
                j += dy
        return bishop_moves

    def get_rook_moves(self, current_pos):
        x, y = current_pos
        rook_moves = []
        color = self.board_logic_array[x][y].islower()

        # Check all 4 directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i, j = x + dx, y + dy
            while 0 <= i < 8 and 0 <= j < 8:
                if self.board_logic_array[i][j] == '.':
                    rook_moves.append((i, j))
                elif self.board_logic_array[i][j].islower() == color:
                    break
                else:
                    rook_moves.append((i, j))
                    break
                i += dx
                j += dy
        return rook_moves

    def get_queen_moves(self, current_pos):
        x, y = current_pos
        queen_moves = []
        color = self.board_logic_array[x][y].islower()

        # Check all 8 directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            i, j = x + dx, y + dy
            while 0 <= i < 8 and 0 <= j < 8:
                if self.board_logic_array[i][j] == '.':
                    queen_moves.append((i, j))
                elif self.board_logic_array[i][j].islower() == color:
                    break
                else:
                    queen_moves.append((i, j))
                    break
                i += dx
                j += dy
        return queen_moves

    def get_king_moves(self, current_pos):
        row, col = current_pos
        # Get the color of the king
        color = self.board_logic_array[row, col].isupper()

        # Define the list of all possible moves for the king
        moves = [(row + i, col + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]

        # Filter out any moves that are not valid
        valid_moves = []
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Make sure the move is within the board
                if self.board_logic_array[r, c] == '.' or self.board_logic_array[r, c].isupper() != color:  # Make sure the square is not occupied by a piece of the same color
                    valid_moves.append((r, c))

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
        board_backup = np.copy(self.board_logic_array)

        # check move
        for move in moves:

            # make test move
            self.test_move(row, col, move[0], move[1])

            # if there is no check, it is legal
            if not self.is_in_check():
                legal_moves.append(move)

            # restore original board
            self.board_logic_array = np.copy(board_backup)

        self.board_logic_array = np.copy(board_backup)

        return legal_moves

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

    def is_my_square_under_attack(self, position):
        # color white -> 1 black -> 0
        for x, y in itertools.product(range(8), range(8)):
            piece = self.board_logic_array[x][y]

            if piece != '.' and piece.isupper() != self.color:
                moves = self.single_piece_move(piece, x, y)

                if (position[0], position[1]) in moves:
                    return True
        return False

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

        print(self.board_logic_array)

    # def get_all_possible_moves(self, x, y):



