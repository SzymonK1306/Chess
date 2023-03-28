from PyQt5.QtGui import QDrag, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QMimeData, QPointF


# Overall class for each piece
class Piece(QGraphicsPixmapItem):
    def __init__(self, color, type, positionX, positionY):
        super().__init__()
        self.color = color
        self.positionX = positionX
        self.positionY = positionY
        self.type = type

        match type:
            case 'Pawn':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Rook':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Knight':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Bishop':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_bishop.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_bishop.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Queen':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_queen.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_queen.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'King':
                if color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_king.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap('images/white_king.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.setPos(self.positionX, positionY)

    # PROTOTYPE OF DRAGGING
        # if self.color == 'w':
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mousePressEvent(self, event):
        if self.color == self.scene().activePlayer:     # checking color
            if event.button() == Qt.LeftButton:
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                self.drag_start_position = event.scenePos()
                # save start position
                self.drag_start_position = QPointF(self.drag_start_position.x()//100 * 100, self.drag_start_position.y()//100 * 100)
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.color == self.scene().activePlayer:     # checking color
            super().mouseMoveEvent(event)
            # if event.buttons() & Qt.LeftButton:
            #     pos = event.scenePos()
                # self.setPos(pos.x() - self.rect().width() / 2, pos.y() - self.rect().height() / 2)
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         drag_distance = (event.scenePos() - self.drag_start_position).manhattanLength()
    #         if drag_distance >= QApplication.startDragDistance():
    #             # drag = QDrag(event.widget())
    #             # mime_data = QMimeData()
    #             # drag.setMimeData(mime_data)
    #             # drag.setPixmap(self.grab())
    #             # drag.setHotSpot(event.pos())
    #             # drag.exec(Qt.CopyAction)
    #             pass
    #     super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.color == self.scene().activePlayer: # checking color
            if event.button() == Qt.LeftButton:
                self.setCursor(QCursor(Qt.OpenHandCursor))
                drop_position = event.scenePos()
                drop_x = int(drop_position.x() / 100)
                drop_y = int(drop_position.y() / 100)
                new_pos = QPointF(drop_x * 100, drop_y * 100)
                self.setPos(new_pos)
                # checking if the move was made
                if self.drag_start_position != new_pos:
                    print(self.drag_start_position)
                    if self.color == 'white':
                        self.scene().activePlayer = 'black'
                    else:
                        self.scene().activePlayer = 'white'
                    print(self.scene().activePlayer)
            super().mouseReleaseEvent(event)


