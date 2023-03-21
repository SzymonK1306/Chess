from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from piece import Piece


# Rook class
class Rook(Piece):
    def __init__(self, color, positionX, positionY):
        super().__init__(color, positionX, positionY)
        if color == 'b':
            self.setPixmap(QPixmap('images/black_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(QPixmap('images/white_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

