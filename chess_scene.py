from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMenu, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from piece import Piece
from logic import ChessLogic
from field import Field
import numpy as np


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
        self.white_pawns = [Piece('white', 'Pawn', 100 * i, 600) for i in range(8)]
        self.white_bishops = [Piece('white', 'Bishop', 200, 700), Piece('white', 'Bishop', 500, 700)]
        self.white_knights = [Piece('white', 'Knight', 100, 700), Piece('white', 'Knight', 600, 700)]
        self.white_rooks = [Piece('white', 'Rook', 0, 700), Piece('white', 'Rook', 700, 700)]
        self.white_queens = [Piece('white', 'Queen',  300, 700)]
        self.white_king = Piece('white', 'King', 400, 700)
        # print(type(self.white_king))

        # black pieces
        self.black_pawns = [Piece('black', 'Pawn', 100 * i, 100) for i in range(8)]
        self.black_bishops = [Piece('black', 'Bishop', 200, 0), Piece('black', 'Bishop', 500, 0)]
        self.black_knights = [Piece('black', 'Knight', 100, 0), Piece('black', 'Knight', 600, 0)]
        self.black_rooks = [Piece('black', 'Rook', 0, 0), Piece('black', 'Rook', 700, 0)]
        self.black_queens = [Piece('black', 'Queen',  300, 0)]
        self.black_king = Piece('black', 'King', 400, 0)

        # add to scene
        [self.addItem(piece) for piece in self.black_pawns]
        [self.addItem(piece) for piece in self.black_bishops]
        [self.addItem(piece) for piece in self.black_knights]
        [self.addItem(piece) for piece in self.black_rooks]
        [self.addItem(piece) for piece in self.black_queens]
        self.addItem(self.black_king)

        [self.addItem(piece) for piece in self.white_pawns]
        [self.addItem(piece) for piece in self.white_bishops]
        [self.addItem(piece) for piece in self.white_knights]
        [self.addItem(piece) for piece in self.white_rooks]
        [self.addItem(piece) for piece in self.white_queens]
        self.addItem(self.white_king)

        self.napis = 'pisze'
        self.activePlayer = 'white'
        self.chess_board = ChessLogic()

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


    def highlight_moves(self, possible_moves):
        for i in range(len(possible_moves)):
            coordinates = possible_moves[i]
            self.board[int(coordinates[1]) * 8 + int(coordinates[0])].highlight_field()

    def unhighlight_moves(self, possible_moves):
        for i in range(len(possible_moves)):
            coordinates = possible_moves[i]
            self.board[int(coordinates[1]) * 8 + int(coordinates[0])].unhighlight_field()

    def active_player_information(self, text):
        self.textChanged.emit(text)

    def pieces_positions(self):
        for scene_item in self.items():
            x = scene_item.positionX
            y = scene_item.positionY
            color = scene_item.color

