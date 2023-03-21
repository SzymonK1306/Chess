from PyQt5.QtWidgets import QGraphicsPixmapItem


# Overall class for each piece
class Piece(QGraphicsPixmapItem):
    def __init__(self, color, positionX, positionY):
        super().__init__()
        self.color = color
        self.positionX = positionX
        self.positionY = positionY

        self.setPos(self.positionX, positionY)
