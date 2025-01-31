import sqlite3
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QLineEdit, QMessageBox, QComboBox, QGraphicsView
from PyQt5 import uic
from history.playback import Playback_Scene


class HistoryWindow(QDialog):
    def __init__(self, game_title, parent=None):
        super().__init__(parent)

        uic.loadUi('history/history.ui', self)

        self.game_title = game_title

        # choose the file to load
        if self.game_title[9] == 'S':
            # change game title (only date)
            self.game_title = self.game_title[14:]
            self.list_of_moves = self.load_sql()
        else:
            # change game title (only date)
            self.game_title = self.game_title[14:]
            self.list_of_moves = self.load_xml()

        self.main_graphic = self.findChild(QGraphicsView, 'main_graphic')

        self.scene = Playback_Scene(self)
        self.scene.init_board()

        self.main_graphic.setScene(self.scene)

        # Next button
        self.next_button = self.findChild(QPushButton, 'next_button')
        self.next_button.clicked.connect(self.make_move)

        self.current_move = 0

    def load_sql(self):
        # load saved histories
        conn = sqlite3.connect('history/chess_game.db')
        cursor = conn.cursor()

        cursor.execute("SELECT move FROM moves WHERE game_id = (?)", (self.game_title,))

        # Fetch all the dates from the query result
        move_list = cursor.fetchall()

        cursor.close()
        conn.close()

        move_list = [move[0] for move in move_list]

        print(move_list)

        return move_list

    def load_xml(self):
        # read the XML file into a string
        with open('history/chess_game.xml', 'r') as f:
            xml_str = f.read()

        # parse the XML string into an ElementTree object
        root = ET.fromstring(xml_str)

        # extract the move elements into a list
        move_list = [move.text for move in root.findall('move')]

        # print the move list
        print(move_list)

        return move_list

    def make_move(self):
        if self.current_move < len(self.list_of_moves):
            self.scene.use_chess_notation(self.list_of_moves[self.current_move])
            self.current_move += 1
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle('All saved moves done')
            message_box.setText('Close history window and see all again')
            message_box.exec()
