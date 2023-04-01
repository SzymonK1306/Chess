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
        self.possible_moves = []

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
                self.setOpacity(0.5)
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                self.drag_start_position = event.scenePos()

                # save start position
                piece_x = self.drag_start_position.x()//100
                piece_y = self.drag_start_position.y() // 100
                self.drag_start_position = QPointF(piece_x * 100, piece_y * 100)

                # possible moves
                self.possible_moves = self.scene().chess_board.get_piece_moves(int(piece_y), int(piece_x))

                self.scene().highlight_moves(self.possible_moves)
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.color == self.scene().activePlayer:     # checking color
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.color == self.scene().activePlayer:     # checking color
            if event.button() == Qt.LeftButton:
                self.setOpacity(1.0)
                # unhighlight fields
                self.scene().unhighlight_moves(self.possible_moves)

                self.setCursor(QCursor(Qt.OpenHandCursor))
                drop_position = event.scenePos()
                drop_x = int(drop_position.x() / 100)
                drop_y = int(drop_position.y() / 100)
                new_pos = QPointF(drop_x * 100, drop_y * 100)

                # check move is correct
                correct_flag = False
                for i in range(len(self.possible_moves)):
                    coordinates = self.possible_moves[i]
                    if drop_x == coordinates[1] and drop_y == coordinates[0]:
                        correct_flag = True
                        break

                if correct_flag:
                    # if self.is_check:
                    #     self.scene().unhighlight_moves(self.king_position)
                    if self.color == 'black':
                        self.scene().unhighlight_king(1)
                    else:
                        self.scene().unhighlight_king(0)
                    captured_item = [item for item in self.scene().items(new_pos, 100, 100) if isinstance(item, Piece) and item is not self]
                    if captured_item:
                        self.scene().removeItem(captured_item[0])
                    self.setPos(new_pos)
                    # checking if the move was made
                    if self.drag_start_position != new_pos:
                        # move in np.array
                        self.scene().chess_board.move(int(self.drag_start_position.y()/100), int(self.drag_start_position.x()/100),
                                                       int(new_pos.y()/100), int(new_pos.x()/100))

                        # enemy in check
                        if self.color == 'black':
                            self.scene().is_check, self.scene().black_king_position = self.scene().chess_board.is_check()
                            if self.scene().is_check:
                                self.scene().check_highlight(0)
                        else:
                            self.scene().is_check, self.scene().white_king_position = self.scene().chess_board.is_check()
                            if self.scene().is_check:
                                self.scene().check_highlight(1)

                        print(self.scene().is_check, self.color)

                        # change sites
                        if self.color == 'white':
                            self.scene().activePlayer = 'black'
                        else:
                            self.scene().activePlayer = 'white'
                        # print(self.is_check)
                        # self.scene().unhighlight_moves(self.king_position)
                else:
                    self.setPos(self.drag_start_position)
                self.possible_moves.clear()
            super().mouseReleaseEvent(event)


