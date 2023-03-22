from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMenu, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from pawn import Pawn
from bishop import Bishop
from knight import Knight
from rook import Rook
from queen import Queen
from king import King
from field import Field


# main class scene
class Chess_Scene(QGraphicsScene):
    def __int__(self):
        super().__init__()
        self.board_number = 1

    def init_board(self):
        # board generation
        # self.board = QGraphicsPixmapItem()
        # self.board.setPixmap(QPixmap(":/board/board.png").scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.addItem(self.board)

        self.board = [Field(i, j) for i in range(8) for j in range(8)]
        [self.addItem(single_field) for single_field in self.board]

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

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setTitle("Change")

        board_menu = QMenu("Board", menu)
        pieces_menu = QMenu("Pieces", menu)

        change_board1_action = QAction("Brown-white", board_menu)
        change_board2_action = QAction("Blue-white", board_menu)
        board_menu.addAction(change_board1_action)
        board_menu.addAction(change_board2_action)

        change_pieces1_action = QAction("Black-White pieces", pieces_menu)
        change_pieces2_action = QAction("Red-White pieces", pieces_menu)
        pieces_menu.addAction(change_pieces1_action)
        pieces_menu.addAction(change_pieces2_action)

        menu.addMenu(board_menu)
        menu.addMenu(pieces_menu)

        action = menu.exec(event.screenPos())

        if action == change_board1_action:
            # self.board.setPixmap(QPixmap(":/board/board.png").scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            [single_field.black_fields() for single_field in self.board]
        elif action == change_board2_action:
            # self.board.setPixmap(QPixmap("images/board2_new.png").scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            [single_field.blue_fields() for single_field in self.board]
        elif action == change_pieces1_action:
            self.black_king.setPixmap(QPixmap("images/black_king.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            [piece.setPixmap(QPixmap("images/black_pawn.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_pawns]
            [piece.setPixmap(QPixmap("images/black_bishop.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_bishops]
            [piece.setPixmap(QPixmap("images/black_knight.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_knights]
            [piece.setPixmap(QPixmap("images/black_rook.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_rooks]
            [piece.setPixmap(QPixmap("images/black_queen.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_queens]
        elif action == change_pieces2_action:
            self.black_king.setPixmap(QPixmap("images/red_king.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            [piece.setPixmap(QPixmap("images/red_pawn.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_pawns]
            [piece.setPixmap(QPixmap("images/red_bishop.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_bishops]
            [piece.setPixmap(QPixmap("images/red_knight.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_knights]
            [piece.setPixmap(QPixmap("images/red_rook.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_rooks]
            [piece.setPixmap(QPixmap("images/red_queen.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) for piece in self.black_queens]
