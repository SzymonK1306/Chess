import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QGraphicsView, QRadioButton
from PyQt5.QtCore import QRegExp
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QRegExpValidator
from chess_scene import Chess_Scene
from clock import Clock
from config import ConfigWindow


class Form(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Form, self).__init__()

        uic.loadUi('mainWindow.ui', self)

        self.setWindowTitle('Chess')

        # find elements in .ui
        self.main_graphic = self.findChild(QGraphicsView, 'main_graphic')

        self.white_clock_view = self.findChild(QGraphicsView, 'white_clock_view')
        self.black_clock_view = self.findChild(QGraphicsView, 'black_clock_view')

        # notation reading elements
        self.chess_notation_line = self.findChild(QLineEdit, 'chess_notation_edit')
        self.chess_notation_button = self.findChild(QPushButton, 'chess_notation_button')

        regex = QRegExp("^([KQNBRAH]?[A-Ha-h][1-8]-[a-h][1-8])$")

        validator = QRegExpValidator(regex, self.chess_notation_line)
        self.chess_notation_line.setValidator(validator)

        self.chess_notation_button.clicked.connect(self.chess_notation)

        self.white_clock_scene = Clock('white', self)
        self.black_clock_scene = Clock('black', self)

        self.white_clock_view.setScene(self.white_clock_scene)
        self.black_clock_view.setScene(self.black_clock_scene)
        # self.title_label = self.findChild(QLabel, 'title_label')
        # RC file
        # QResource.registerResource("images/data.qrc")

        # create the icon object
        icon = QIcon("images/red_king.png")

        # set the application icon
        QApplication.setWindowIcon(icon)

        # scene creation
        self.scene = Chess_Scene(self)

        # initial board state
        self.scene.init_board()

        self.main_graphic.setScene(self.scene)

        # game config dialog
        self.game_mode = None

        self.config_dialog = ConfigWindow(self)
        self.config_dialog.exec()

        print(self.game_mode)

    def chess_notation(self):
        chess_notation_text = self.chess_notation_line.text()
        self.scene.use_chess_notation(chess_notation_text)
        self.chess_notation_line.clear()

    # def open_dialog(self):
    #     # Load the dialog UI file
    #     dialog = uic.loadUi('config.ui')
    #
    #     dialog.radio_button_single = dialog.findChild(QRadioButton, 'radioButton_single')
    #     dialog.radio_button_two = dialog.findChild(QRadioButton, 'radioButton_two')
    #     dialog.radio_button_ai = dialog.findChild(QRadioButton, 'radioButton_ai')
    #
    #     dialog.save_button = dialog.findChild(QPushButton, 'start_button_game')
    #     dialog.save_button.clicked.connect(lambda: self.save_radio_selection(dialog))
    #     # Show the dialog
    #     dialog.exec()
    #
    # def save_radio_selection(self, dialog):
    #     # Find which radio button is checked and save the selection
    #     if dialog.radio_button_single.isChecked():
    #         selection = 'Single player selected'
    #     elif dialog.radio_button_two.isChecked():
    #         selection = 'Two players selected'
    #     elif dialog.radio_button_ai.isChecked():
    #         selection = 'AI selected'
    #     else:
    #         selection = 'No radio button selected'
    #     # Print the selection (you could also save it to a file or database)
    #     print(selection)
    #     # Close the dialog
    #     dialog.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
