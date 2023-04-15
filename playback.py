from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMenu, QAction, QGraphicsTextItem, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from piece import Piece
from logic import ChessLogic
from field import Field
from promotion import PromotionDialog
import data_rc
import numpy as np


# main class scene
class Playback_Scene(QGraphicsScene):
    def __int__(self):
        super().__init__()
        self.board_number = 1

    def init_board(self):
        """
        Create pieces and initial state of the game
        :return:
        """

        # create board
        self.board = [Field(i, j) for i in range(8) for j in range(8)]
        [self.addItem(single_field) for single_field in self.board]

        # white pieces
        self.white_pawns = [Piece('white', 'Pawn', 100 * i, 600) for i in range(8)]
        self.white_bishops = [Piece('white', 'Bishop', 200, 700), Piece('white', 'Bishop', 500, 700)]
        self.white_knights = [Piece('white', 'Knight', 100, 700), Piece('white', 'Knight', 600, 700)]
        self.white_rooks = [Piece('white', 'Rook', 0, 700), Piece('white', 'Rook', 700, 700)]
        self.white_queens = [Piece('white', 'Queen',  300, 700)]
        self.white_king = Piece('white', 'King', 400, 700)

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

        # add description of each row and column
        self.text_init()

        # This scene is only for visualisation
        self.activePlayer = None

        # create logic class object
        self.chess_board = ChessLogic()

        # there is no check
        self.is_check = False

        # save kings positions
        self.white_king_position = [(7, 4)]
        self.black_king_position = [(0, 4)]

    def check_highlight(self, color):
        """
        Red highlight field with the king which is in check
        :param color: white - True, black - false
        :return:
        """

        # get king position
        if color:
            kingX, kingY = self.white_king_position[0]
        else:
            kingX, kingY = self.black_king_position[0]

        # highlight field with king
        self.board[int(kingY) * 8 + int(kingX)].red_highlight()

    def unhighlight_king(self, color):
        """
        Unhighlight field after check
        :param color: white - True, black - false
        :return:
        """
        if color:
            self.board[int(self.white_king_position[0][1]) * 8 + int(self.white_king_position[0][0])].unhighlight_field()
        else:
            self.board[int(self.black_king_position[0][1]) * 8 + int(self.black_king_position[0][0])].unhighlight_field()

    def text_init(self):
        """
        Add letters and numbers to rows and columns
        :return:
        """
        # create a QGraphicsTextItem
        a_text = QGraphicsTextItem("A")
        b_text = QGraphicsTextItem("B")
        c_text = QGraphicsTextItem("C")
        d_text = QGraphicsTextItem("D")
        e_text = QGraphicsTextItem("E")
        f_text = QGraphicsTextItem("F")
        g_text = QGraphicsTextItem("G")
        h_text = QGraphicsTextItem("H")

        text_1 = QGraphicsTextItem("1")
        text_2 = QGraphicsTextItem("2")
        text_3 = QGraphicsTextItem("3")
        text_4 = QGraphicsTextItem("4")
        text_5 = QGraphicsTextItem("5")
        text_6 = QGraphicsTextItem("6")
        text_7 = QGraphicsTextItem("7")
        text_8 = QGraphicsTextItem("8")


        # set the font and color of the text
        font = QFont("Arial", 12)
        color = QColor(255, 0, 0)  # red

        a_text.setFont(font)
        a_text.setDefaultTextColor(color)
        a_text.setPos(0, 775)
        self.addItem(a_text)

        b_text.setFont(font)
        b_text.setDefaultTextColor(color)
        b_text.setPos(100, 775)
        self.addItem(b_text)

        c_text.setFont(font)
        c_text.setDefaultTextColor(color)
        c_text.setPos(200, 775)
        self.addItem(c_text)

        d_text.setFont(font)
        d_text.setDefaultTextColor(color)
        d_text.setPos(300, 775)
        self.addItem(d_text)

        e_text.setFont(font)
        e_text.setDefaultTextColor(color)
        e_text.setPos(400, 775)
        self.addItem(e_text)

        f_text.setFont(font)
        f_text.setDefaultTextColor(color)
        f_text.setPos(500, 775)
        self.addItem(f_text)

        g_text.setFont(font)
        g_text.setDefaultTextColor(color)
        g_text.setPos(600, 775)
        self.addItem(g_text)

        h_text.setFont(font)
        h_text.setDefaultTextColor(color)
        h_text.setPos(700, 775)
        self.addItem(h_text)

        text_1.setFont(font)
        text_1.setDefaultTextColor(color)
        text_1.setPos(780, 700)
        self.addItem(text_1)

        text_2.setFont(font)
        text_2.setDefaultTextColor(color)
        text_2.setPos(780, 600)
        self.addItem(text_2)

        text_3.setFont(font)
        text_3.setDefaultTextColor(color)
        text_3.setPos(780, 500)
        self.addItem(text_3)

        text_4.setFont(font)
        text_4.setDefaultTextColor(color)
        text_4.setPos(780, 400)
        self.addItem(text_4)

        text_5.setFont(font)
        text_5.setDefaultTextColor(color)
        text_5.setPos(780, 300)
        self.addItem(text_5)

        text_6.setFont(font)
        text_6.setDefaultTextColor(color)
        text_6.setPos(780, 200)
        self.addItem(text_6)

        text_7.setFont(font)
        text_7.setDefaultTextColor(color)
        text_7.setPos(780, 100)
        self.addItem(text_7)

        text_8.setFont(font)
        text_8.setDefaultTextColor(color)
        text_8.setPos(780, 0)
        self.addItem(text_8)