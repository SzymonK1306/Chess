from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from piece import Piece
from PyQt5.QtWidgets import QGraphicsPixmapItem


# King class
class Field(QGraphicsPixmapItem):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.mode = 'black'
        self.piece = None
        if (self.x + self.y) % 2 == 1:
            self.setPixmap(QPixmap('images/black_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        else:
            self.setPixmap(QPixmap('images/white_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # self.setPos(self.x * 100, 700 - self.y * 100)
        self.setPos(self.x * 100, self.y * 100)

    def black_fields(self):
        self.mode = 'black'
        if (self.x + self.y) % 2 == 1:
            self.setPixmap(
                QPixmap('images/black_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def blue_fields(self):
        self.mode = 'blue'
        if (self.x + self.y) % 2 == 1:
            self.setPixmap(
                QPixmap('images/blue_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def highlight_field(self):
        """
        Highlight fields of correct move
        :return: None
        """
        self.setPixmap(
            QPixmap('images/highlighted.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def unhighlight_field(self):
        """
        Unhighlight fields when move is over (or incorrect)
        :return: None
        """
        if (self.x + self.y) % 2 == 1:
            if self.mode == 'black':
                self.setPixmap(
                    QPixmap('images/black_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif self.mode == 'blue':
                self.setPixmap(
                    QPixmap('images/blue_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.setPixmap(
                QPixmap('images/white_field.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

