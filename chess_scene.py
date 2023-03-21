from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pawn import Pawn
from bishop import Bishop
from knight import Knight
from rook import Rook
from queen import Queen
from king import King


# main class scene
class Chess_Scene(QGraphicsScene):
    def __int__(self):
        super().__init__()

    def init_board(self):
        # board generation
        self.board = QGraphicsPixmapItem()
        self.board.setPixmap(QPixmap(":/board/board.png").scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.addItem(self.board)

        # white pieces
        self.white_pawns = [Pawn('w', 100 * i, 600) for i in range(8)]
        self.white_bishops = [Bishop('w', 200, 700), Bishop('w', 500, 700)]
        self.white_knights = [Knight('w', 100, 700), Knight('w', 600, 700)]
        self.white_rooks = [Rook('w', 0, 700), Rook('w', 700, 700)]
        self.white_queens = [Queen('w', 300, 700)]
        self.white_king = King('w', 400, 700)

        # black pieces
        self.black_pawns = [Pawn('b', 100 * i, 100) for i in range(8)]
        self.black_bishops = [Bishop('b', 200, 0), Bishop('b', 500, 0)]
        self.black_knights = [Knight('b', 100, 0), Knight('b', 600, 0)]
        self.black_rooks = [Rook('b', 0, 0), Rook('b', 700, 0)]
        self.black_queens = [Queen('b', 300, 0)]
        self.black_king = King('b', 400, 0)

        # add to scene
        [self.addItem(piece) for piece in self.white_pawns]
        [self.addItem(piece) for piece in self.white_bishops]
        [self.addItem(piece) for piece in self.white_knights]
        [self.addItem(piece) for piece in self.white_rooks]
        [self.addItem(piece) for piece in self.white_queens]
        self.addItem(self.white_king)

        [self.addItem(piece) for piece in self.black_pawns]
        [self.addItem(piece) for piece in self.black_bishops]
        [self.addItem(piece) for piece in self.black_knights]
        [self.addItem(piece) for piece in self.black_rooks]
        [self.addItem(piece) for piece in self.black_queens]
        self.addItem(self.black_king)

