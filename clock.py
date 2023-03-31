from PyQt5.QtGui import QColor, QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, \
    QGraphicsSimpleTextItem
from PyQt5.QtCore import Qt, QTimer, QTime, QPointF
import math

class Clock(QGraphicsScene):
    def __init__(self):
        super().__init__()
        # Create the clock face
        # Set scene size
        self.setSceneRect(0, 0, 300, 300)
        self.gameTime = QTime(0, 10, 0)

        # Set scene background color
        self.setBackgroundBrush(QBrush(Qt.gray))

        # Create stopwatch ellipse item
        self.stopwatch = QGraphicsEllipseItem(0, 0, 250, 250)
        self.stopwatch.setPos(25, 25)
        self.stopwatch.setPen(QPen(Qt.black, 5))
        self.stopwatch.setBrush(QColor(235, 203, 115))
        self.addItem(self.stopwatch)

        # Create minute hand
        self.minuteHand = QGraphicsLineItem(0, 0, 0, -100)
        self.minuteHand.setPen(QPen(Qt.black, 4))
        self.minuteHand.setPos(QPointF(150, 150))
        self.minuteHand.setZValue(2)
        self.addItem(self.minuteHand)

        # Create second hand
        self.secondHand = QGraphicsLineItem(0, 0, 0, -120)
        self.secondHand.setPen(QPen(Qt.red, 2))
        self.secondHand.setPos(QPointF(150, 150))
        self.secondHand.setZValue(3)
        self.addItem(self.secondHand)

        # Create millisecond hand
        self.millisecondHand = QGraphicsLineItem(0, 0, 0, -120)
        self.millisecondHand.setPen(QPen(Qt.red, 2))
        self.millisecondHand.setPos(QPointF(150, 150))
        self.millisecondHand.setZValue(3)
        self.addItem(self.millisecondHand)

        # Create minute markers
        for i in range(60):
            line = QGraphicsLineItem(0, -120, 0, -125)
            line.setPen(QPen(Qt.black, 3))
            line.setPos(QPointF(150, 150))
            line.setRotation(i * 6.0)
            self.addItem(line)

        for minute in range(0, 60, 5):
            angle = math.radians(-6 * minute + 90)
            x = 110 * math.cos(angle) + 150
            y = - 110 * math.sin(angle) + 150
            scaleItem = QGraphicsSimpleTextItem(str(minute))
            scaleItem.setFont(QFont('Arial', 10))
            scaleItem.setPos(x - 7, y - 7)
            self.addItem(scaleItem)

        # Create timer to update clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1)


    def updateClock(self):
        self.gameTime = self.gameTime.addMSecs(-1)

        seconds = self.gameTime.second() + self.gameTime.msec() / 1000.0
        self.secondHand.setRotation(-seconds * 6.0)
        self.minuteHand.setRotation(-self.gameTime.minute() * 6.0 + - seconds / 10.0)
        self.millisecondHand.setRotation(-self.gameTime.msec() * 0.36)

        # Get current time
        # currentTime = QTime.currentTime()
        #
        # # Calculate minute and second angles
        # minuteAngle = (currentTime.minute() / 60) * 360
        # secondAngle = (currentTime.msec() / 60) * 360
        #
        # # Rotate minute and second hands
        # self.minuteHand.setRotation(minuteAngle)
        # self.secondHand.setRotation(secondAngle)
