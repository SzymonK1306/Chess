from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator


class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('config.ui', self)

        # disable close button
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        # RadioButtons
        self.radio_button_single = self.findChild(QRadioButton, 'radioButton_single')
        self.radio_button_two = self.findChild(QRadioButton, 'radioButton_two')
        self.radio_button_ai = self.findChild(QRadioButton, 'radioButton_ai')

        self.radio_button_single.setChecked(True)

        # PushButton
        self.save_button = self.findChild(QPushButton, 'start_button_game')
        self.save_button.clicked.connect(self.save_radio_selection)

        # LineEdit
        self.IP_edit = self.findChild(QLineEdit, 'IP_edit')
        self.port_edit = self.findChild(QLineEdit, 'port_edit')

        # IP mask
        self.IP_edit.setText("127.0.0.1")
        self.IP_edit.setInputMask("000.000.000.000")

        # port mask
        self.port_edit.setText("55555")
        self.port_edit.setInputMask("00000")

    def save_radio_selection(self):
        # Find which radio button is checked and save the selection
        if self.radio_button_single.isChecked():
            selection = 'Single player selected'
        elif self.radio_button_two.isChecked():
            selection = 'Two players selected'
        elif self.radio_button_ai.isChecked():
            selection = 'AI selected'
        else:
            selection = 'No radio button selected'
        # Save information in main window (you could also save it to a file or database)
        self.parent().game_mode = selection
        # Close the dialog
        self.close()

    def keyPressEvent(self, event):
        # Disable the Escape key shortcut
        if event.key() == Qt.Key_Escape:
            event.ignore()
