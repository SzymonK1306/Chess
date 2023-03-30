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

    def get_piece_moves(self, row, col):
        moves = []
        piece = self.board_logic_array[row, col]

        print(piece)

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

        return moves

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




