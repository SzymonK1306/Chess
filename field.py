from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from piece import Piece
from PyQt5.QtWidgets import QGraphicsPixmapItem


# King class
class Field(QGraphicsPixmapItem):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        if (self.x + self.y) % 2 == 0:
            self.setPixmap(QPixmap('images/black_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        else:
            self.setPixmap(QPixmap('images/white_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.setPos(self.x * 100, 700 - self.y * 100)

    def black_fields(self):
        if (self.x + self.y) % 2 == 0:
            self.setPixmap(
                QPixmap('images/black_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def blue_fields(self):
        if (self.x + self.y) % 2 == 0:
            self.setPixmap(
                QPixmap('images/blue_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
