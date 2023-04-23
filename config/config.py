from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QLineEdit, QMessageBox, QComboBox
from PyQt5 import uic
from online.client import ChessClient
from PyQt5.QtCore import Qt, QRegExp
import json
import sqlite3
from history.history import HistoryWindow
# from server import ChessServer
from PyQt5.QtGui import QRegExpValidator, QIntValidator


class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('config/config.ui', self)

        # disable close button
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        # RadioButtons
        self.radio_button_single = self.findChild(QRadioButton, 'radioButton_single')
        self.radio_button_two = self.findChild(QRadioButton, 'radioButton_two')
        self.radio_button_ai = self.findChild(QRadioButton, 'radioButton_ai')

        self.radio_button_two.setChecked(True)

        # PushButtons
        # start
        self.start_button = self.findChild(QPushButton, 'start_button_game')
        self.start_button.clicked.connect(self.start_game)

        # save json
        self.save_button = self.findChild(QPushButton, 'save_options_button')
        self.save_button.clicked.connect(self.save_to_json)

        # load json
        self.load_button = self.findChild(QPushButton, 'load_options_button')
        self.load_button.clicked.connect(self.load_from_json)

        self.load_button = self.findChild(QPushButton, 'start_server_button')
        self.load_button.clicked.connect(self.create_server)

        # load history
        self.history_button = self.findChild(QPushButton, 'load_history_button')
        self.history_button.clicked.connect(self.load_history)

        # comboBox
        self.combo = self.findChild(QComboBox, 'comboBox')

        # server
        # self.server = CommunicatorServer()

        # load saved histories
        conn = sqlite3.connect('history/chess_game.db')
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT game_id FROM moves")

        # Fetch all the dates from the query result
        dates = cursor.fetchall()

        cursor.close()
        conn.close()

        dates = [date[0] for date in dates]

        for date in dates:
            self.combo.addItem('Saved in SQL: ' + date)

        self.combo.addItem('Saved in XML: chess_game.xml')

        # LineEdit
        self.IP_edit = self.findChild(QLineEdit, 'IP_edit')
        self.port_edit = self.findChild(QLineEdit, 'port_edit')

        # IP mask
        # self.IP_edit.setText("2a00:f41:4864:9a0b:8f7b:40bc:4cd3:a563")
        self.IP_edit.setText("127.0.0.1")
        self.IP_edit.setInputMask("000.000.000.000")

        # port mask
        self.port_edit.setText("5000")
        self.port_edit.setInputMask("00000")

    def create_server(self):
        IP_address = self.IP_edit.text()
        port = self.port_edit.text()
        self.server.start_server(IP_address, port)

    def load_history(self):
        self.history_dialog = HistoryWindow(self.combo.currentText(), self)
        self.history_dialog.exec()

    def load_from_json(self):
        with open('config/game_options.json') as f:
            options = json.load(f)

        game_type = options['game_type']
        ip_address = options['IP_address']
        port = options['port']

        if game_type == 'Single player':
            self.radio_button_single.setChecked(True)
        elif game_type == 'Two players':
            self.radio_button_two.setChecked(True)
        elif game_type == 'AI':
            self.radio_button_ai.setChecked(True)

        self.IP_edit.setText(ip_address)
        self.port_edit.setText(str(port))

        message_box = QMessageBox()
        message_box.setWindowTitle('Success')
        message_box.setText('Options loaded successfully')
        message_box.exec()

    def save_to_json(self):
        game_type = self.load_info_radio_buttons()
        IP_address = self.IP_edit.text()
        port = self.port_edit.text()

        options = {
            'game_type': game_type,
            'IP_address': IP_address,
            'port': int(port)
        }

        with open('config/game_options.json', 'w') as f:
            json_string = json.dumps(options)
            f.write(json_string)

        message_box = QMessageBox()
        message_box.setWindowTitle('Success')
        message_box.setText('Options saved successfully')
        message_box.exec()

    def start_game(self):
        # Find which radio button is checked and save the selection
        selection = self.load_info_radio_buttons()
        # Save information in main window (you could also save it to a file or database)
        self.parent().game_mode = selection
        self.parent().IP_address = self.IP_edit.text()
        self.parent().port = self.port_edit.text()

        # connect to server
        if selection == 'Two players':
            self.parent().client = ChessClient(self.IP_edit.text(), int(self.port_edit.text()), self.parent())
        # Close the dialog
        self.close()

    def load_info_radio_buttons(self):
        if self.radio_button_single.isChecked():
            selection = 'Single player'
        elif self.radio_button_two.isChecked():
            selection = 'Two players'
        elif self.radio_button_ai.isChecked():
            selection = 'AI'
        else:
            selection = 'No radio button selected'

        return selection

    def keyPressEvent(self, event):
        # Disable the Escape key shortcut
        if event.key() == Qt.Key_Escape:
            event.ignore()
