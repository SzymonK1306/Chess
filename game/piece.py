from PyQt5.QtGui import QDrag, QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QApplication
from PyQt5.QtCore import Qt, QMimeData, QPointF


# Overall class for each piece
class Piece(QGraphicsPixmapItem):
    def __init__(self, color, type, positionX, positionY):
        super().__init__()

        self.color = color      # 'white' or 'black'

        # position on board (QGraphicsScene)
        self.positionX = positionX
        self.positionY = positionY

        self.type = type    # 'Pawn', 'Bishop', 'Knight', 'Rook', 'Queen', 'King'

        # empty list of possible moves
        self.possible_moves = []

        # match graphic to the type of piece
        self.match_image()

        self.setPos(self.positionX, positionY)

        # All pieces can be moved by mouse
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mousePressEvent(self, event):
        """
        Behavior after left click
        :param event:
        :return:
        """
        self.drag_start_position = event.scenePos()
        piece_x = self.drag_start_position.x() // 100
        piece_y = self.drag_start_position.y() // 100
        self.drag_start_position = QPointF(piece_x * 100, piece_y * 100)

        # Online configuration
        # Permission for move
        self.permission = False
        if self.color == 'white' and self.scene().white_permission:
            self.permission = True
        elif self.color == 'black' and self.scene().black_permission:
            self.permission = True

        if (self.color == self.scene().activePlayer) and self.permission:     # checking color
            if event.button() == Qt.LeftButton:
                # cosmetic
                self.setOpacity(0.5)
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                self.drag_start_position = event.scenePos()

                # save start position ???
                piece_x = self.drag_start_position.x()//100
                piece_y = self.drag_start_position.y() // 100
                self.drag_start_position = QPointF(piece_x * 100, piece_y * 100)

                # possible moves from chess logic object
                self.possible_moves = self.scene().chess_board.get_piece_moves(int(piece_y), int(piece_x))

                self.scene().highlight_moves(self.possible_moves)
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self.color == self.scene().activePlayer) and self.permission:     # checking color
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Behavior after release
        :param event:
        :return:
        """
        if self.color == self.scene().activePlayer:     # checking color
            if event.button() == Qt.LeftButton:

                # cosmetic
                self.setOpacity(1.0)
                self.setCursor(QCursor(Qt.OpenHandCursor))

                # unhighlight fields
                self.scene().unhighlight_moves(self.possible_moves)

                # calculate position of object after release (in the middle of the field)
                drop_position = event.scenePos()
                drop_x = int(drop_position.x() / 100)
                drop_y = int(drop_position.y() / 100)
                new_pos = QPointF(drop_x * 100, drop_y * 100)

                # check move is correct
                # correct_flag = False
                # for i in range(len(self.possible_moves)):
                #     coordinates = self.possible_moves[i]
                #     if drop_x == coordinates[1] and drop_y == coordinates[0]:
                #         correct_flag = True
                #         break

                # when move was correct
                if (drop_y, drop_x) in self.possible_moves:

                    # unhighlight king field (if move was correct then can not be in check)
                    if self.color == 'black':
                        self.scene().unhighlight_king(1)
                    else:
                        self.scene().unhighlight_king(0)

                    # find captured piece
                    captured_item = [item for item in self.scene().items(new_pos, 100, 100) if isinstance(item, Piece) and item is not self]

                    # if founded, delete it
                    if captured_item:
                        self.scene().removeItem(captured_item[0])

                    self.setPos(new_pos)

                    # checking if the move was made
                    if self.drag_start_position != new_pos:
                        # move in chess logic object
                        self.scene().chess_board.move(int(self.drag_start_position.y()/100),
                                                      int(self.drag_start_position.x()/100),
                                                      int(new_pos.y()/100),
                                                      int(new_pos.x()/100))

                        # en passant in scene
                        if self.scene().chess_board.was_en_passant:
                            if self.color == 'white':
                                en_passant_pawn = [item for item in self.scene().items(QPointF(new_pos.x(), new_pos.y() + 100), 100, 100)
                                                   if isinstance(item, Piece)]
                                self.scene().removeItem(en_passant_pawn[0])
                                self.scene().chess_board.was_en_passant = False
                            else:
                                en_passant_pawn = [item for item in self.scene().items(QPointF(new_pos.x(), new_pos.y() - 100), 100, 100)
                                                   if isinstance(item, Piece)]
                                self.scene().removeItem(en_passant_pawn[0])
                                self.scene().chess_board.was_en_passant = False

                        # made castling
                        self.made_castling()
                        if self.color == 'white':
                            if self.scene().chess_board.white_right_castling_available:
                                self.scene().chess_board.white_right_castling_available = False
                            if self.scene().chess_board.white_left_castling_available:
                                self.scene().chess_board.white_left_castling_available = False
                        else:
                            if self.scene().chess_board.black_right_castling_available:
                                self.scene().chess_board.black_right_castling_available = False
                            if self.scene().chess_board.black_left_castling_available:
                                self.scene().chess_board.black_left_castling_available = False

                        # checking promotion
                        if self.type == 'Pawn':
                            promotion_pos = self.scene().chess_board.white_promotion if self.color == 'white' else self.scene().chess_board.black_promotion
                            if len(promotion_pos) != 0:
                                self.scene().pawn_promotion(promotion_pos, self.color)
                                self.scene().chess_board.white_promotion = []
                                self.scene().chess_board.black_promotion = []

                        # enemy in check
                        if self.color == 'black':
                            self.scene().is_check, self.scene().black_king_position = self.scene().chess_board.is_check()
                            if self.scene().is_check:
                                self.scene().check_highlight(0)
                        else:
                            self.scene().is_check, self.scene().white_king_position = self.scene().chess_board.is_check()
                            if self.scene().is_check:
                                self.scene().check_highlight(1)

                        # save IP move
                        # self.scene().ip_move = str(int(self.drag_start_position.x()/100)) + str(int(self.drag_start_position.y()/100)) + str(int(new_pos.x()/100)) + str(int(new_pos.y()/100))
                        # My notation
                        self.scene().ip_move = f'{int(self.drag_start_position.y()/100)}{int(self.drag_start_position.x()/100)}{int(new_pos.y()/100)}{int(new_pos.x()/100)}'
                        print(self.scene().ip_move)
                        # self.scene().parent().client.sendData(self.scene().ip_move)

                        # change sites
                        if self.color == 'white':
                            self.scene().activePlayer = 'white_clock'
                        else:
                            self.scene().activePlayer = 'black_clock'

                # when move wasn't made, put on the start
                else:
                    self.setPos(self.drag_start_position)

                # clear move list
                self.possible_moves.clear()
            super().mouseReleaseEvent(event)

    def change_piece(self, type):
        self.type = type
        self.match_image()
        print(self.type)

    def made_castling(self):
        if self.color == 'white':
            if self.scene().chess_board.white_right_castling_done:
                castling_rook = [item for item in self.scene().items(QPointF(700, 700), 100, 100) if
                                 isinstance(item, Piece)]
                castling_rook[0].setPos(QPointF(500, 700))
                self.scene().chess_board.white_right_castling_done = False

            if self.scene().chess_board.white_left_castling_done:
                castling_rook = [item for item in self.scene().items(QPointF(0, 700), 100, 100) if
                                 isinstance(item, Piece)]
                castling_rook[0].setPos(QPointF(300, 700))
                self.scene().chess_board.white_left_castling_done = False

        else:
            if self.scene().chess_board.black_right_castling_done:
                castling_rook = [item for item in self.scene().items(QPointF(700, 0), 100, 100) if
                                 isinstance(item, Piece)]
                castling_rook[0].setPos(QPointF(500, 0))
                self.scene().chess_board.black_right_castling_done = False

            if self.scene().chess_board.black_left_castling_done:
                castling_rook = [item for item in self.scene().items(QPointF(0, 0), 100, 100) if
                                 isinstance(item, Piece)]
                castling_rook[0].setPos(QPointF(300, 0))
                self.scene().chess_board.black_left_castling_done = False

    def match_image(self):
        match self.type:
            case 'Pawn':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap('images/black_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_pawn.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Rook':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap(':/black_pieces/black_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_rook.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Knight':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap(':/black_pieces/black_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_knight.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Bishop':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap(':/black_pieces/black_bishop.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_bishop.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'Queen':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap(':/black_pieces/black_queen.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_queen.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            case 'King':
                if self.color == 'black':
                    self.setPixmap(
                        QPixmap(':/black_pieces/black_king.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.setPixmap(
                        QPixmap(':/white_pieces/white_king.png').scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

