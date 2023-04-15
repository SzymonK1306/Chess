import sqlite3
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QLineEdit, QMessageBox, QComboBox, QGraphicsView
from PyQt5 import uic
from playback import Playback_Scene


class HistoryWindow(QDialog):
    def __init__(self, game_title, parent=None):
        super().__init__(parent)

        uic.loadUi('history.ui', self)

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

    def load_sql(self):
        # load saved histories
        conn = sqlite3.connect('chess_game.db')
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
        with open('chess_game.xml', 'r') as f:
            xml_str = f.read()

        # parse the XML string into an ElementTree object
        root = ET.fromstring(xml_str)

        # extract the move elements into a list
        move_list = [move.text for move in root.findall('move')]

        # print the move list
        print(move_list)
