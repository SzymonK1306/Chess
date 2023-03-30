import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtCore import QFile, QObject, Qt, QResource
from PyQt5 import QtWidgets, uic
from PySide6.QtUiTools import QUiLoader
from PyQt5.QtGui import QPixmap, QIcon
from chess_scene import Chess_Scene
import data_rc


class Form(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Form, self).__init__()

        uic.loadUi('mainWindow.ui', self)

        # find elements in .ui
        self.main_graphic = self.findChild(QGraphicsView, 'main_graphic')
        # self.title_label = self.findChild(QLabel, 'title_label')
        # RC file
        # QResource.registerResource("images/data.qrc")

        # create the icon object
        icon = QIcon("images/red_king.png")

        # set the application icon
        QApplication.setWindowIcon(icon)

        # scene creation
        self.scene = Chess_Scene()

        # initial board state
        self.scene.init_board()

        self.main_graphic.setScene(self.scene)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
