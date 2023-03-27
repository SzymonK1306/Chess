from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QMimeData, QPointF


# Overall class for each piece
class Piece(QGraphicsPixmapItem):
    def __init__(self, color, positionX, positionY):
        super().__init__()
        self.color = color
        self.positionX = positionX
        self.positionY = positionY

        self.setPos(self.positionX, positionY)

    # PROTOTYPE OF DRAGGING
        if self.color == 'w':
            self.setFlag(QGraphicsItem.ItemIsMovable)
            self.setAcceptHoverEvents(True)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.scenePos()
        super().mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         drag_distance = (event.scenePos() - self.drag_start_position).manhattanLength()
    #         if drag_distance >= QApplication.startDragDistance():
    #             drag = QDrag(event.widget())
    #             mime_data = QMimeData()
    #             drag.setMimeData(mime_data)
    #             drag.setPixmap(self.grab())
    #             drag.setHotSpot(event.pos())
    #             drag.exec(Qt.CopyAction)
    #     super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            drop_position = event.scenePos()
            drop_x = int(drop_position.x() / 100)
            drop_y = int(drop_position.y() / 100)
            new_pos = QPointF(drop_x * 100, drop_y * 100)
            self.setPos(new_pos)
        super().mouseReleaseEvent(event)

