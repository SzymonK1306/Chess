from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from piece import Piece


# Knight class
class Knight(Piece):
    def __init__(self, color, positionX, positionY):
        super().__init__(color, positionX, positionY)
        if color == 'b':
            self.setPixmap(QPixmap('images/black_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(QPixmap('images/white_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

