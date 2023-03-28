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

    def move(self, startX, startY, stopX, stopY):
        piece = self.board_logic_array[startX, startY]
        self.board_logic_array[startX, startY] = '.'
        self.board_logic_array[stopX, stopY] = piece
        print(self.board_logic_array)

    def get_pawn_moves(self, row, col):

        moves = []
        piece = self.board_logic_array[row, col]

        print(piece)

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

        # Check diagonal capture moves
        if col > 0 and row + direction >= 0 and row + direction <= 7:
            if self.board_logic_array[row + direction, col - 1].islower():
                moves.append((row + direction, col - 1))
        if col < 7 and row + direction >= 0 and row + direction <= 7:
            if self.board_logic_array[row + direction, col + 1].islower():
                moves.append((row + direction, col + 1))

        return moves


