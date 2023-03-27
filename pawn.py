from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsRectItem

from piece import Piece


# Pawn class
class Pawn(Piece):
    def __init__(self, color, positionX, positionY):
        super(Pawn, self).__init__(color, positionX, positionY)
        if color == 'b':
            self.setPixmap(QPixmap('images/black_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(QPixmap('images/white_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # PROTOTYPE OF HIGHLIGHTING
    # def mousePressEvent(self, event):
    #     self.highlight_moves()
    #
    # def highlight_moves(self):
    #     # Determine the valid moves for the pawn
    #     valid_moves = []
    #     if self.positionX == 1:
    #         valid_moves.append((self.positionX + 1, self.positionY))
    #         valid_moves.append((self.positionX + 2, self.positionY))
    #     else:
    #         valid_moves.append((self.positionX + 1, self.positionY))
    #
    #     # Check diagonals for capturing
    #     if self.positionY > 0:
    #         valid_moves.append((self.positionX + 1, self.positionY - 1))
    #     if self.positionY < 7:
    #         valid_moves.append((self.positionX + 1, self.positionY + 1))
    #
    #     # Highlight the valid moves on the chess board
    #     for move in valid_moves:
    #         row, col = move
    #         x = col * 100
    #         y = row * 100
    #         # Create a QGraphicsRectItem to draw the highlight
    #         highlight = QGraphicsRectItem(x, y, 100, 100, self)
    #         highlight.setBrush(QBrush(QColor(255, 0, 0, 128)))
