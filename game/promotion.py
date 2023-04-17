from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class PromotionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose Promotion Piece")
        self.setFixedSize(300, 400)  # Set the size of the dialog box

        # Create labels and images for each piece
        queen_label = QLabel(self)
        queen_label.setPixmap(QPixmap("images/white_queen.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Set the path of the image file
        queen_label.setFixedSize(100, 100)  # Set the size of the image
        queen_label.setAlignment(Qt.AlignCenter)

        rook_label = QLabel(self)
        rook_label.setPixmap(QPixmap("images/white_rook.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        rook_label.setFixedSize(100, 100)
        rook_label.setAlignment(Qt.AlignCenter)

        bishop_label = QLabel(self)
        bishop_label.setPixmap(QPixmap("images/white_bishop.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        bishop_label.setFixedSize(100, 100)
        bishop_label.setAlignment(Qt.AlignCenter)

        knight_label = QLabel(self)
        knight_label.setPixmap(QPixmap("images/white_knight.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        knight_label.setFixedSize(100, 100)
        knight_label.setAlignment(Qt.AlignCenter)

        # Create buttons for each piece
        queen_button = QPushButton("Queen", self)
        queen_button.setFixedSize(100, 50)  # Set the size of the button

        rook_button = QPushButton("Rook", self)
        rook_button.setFixedSize(100, 50)

        bishop_button = QPushButton("Bishop", self)
        bishop_button.setFixedSize(100, 50)

        knight_button = QPushButton("Knight", self)
        knight_button.setFixedSize(100, 50)

        # Create vertical layouts for the labels and buttons
        label_layout = QVBoxLayout()
        label_layout.addWidget(queen_label)
        label_layout.addWidget(rook_label)
        label_layout.addWidget(bishop_label)
        label_layout.addWidget(knight_label)

        button_layout = QVBoxLayout()
        button_layout.addWidget(queen_button)
        button_layout.addWidget(rook_button)
        button_layout.addWidget(bishop_button)
        button_layout.addWidget(knight_button)

        # Create a horizontal layout to organize the vertical layouts
        layout = QHBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        queen_button.clicked.connect(self.choose_queen)
        rook_button.clicked.connect(self.choose_rook)
        bishop_button.clicked.connect(self.choose_bishop)
        knight_button.clicked.connect(self.choose_knight)

    def choose_queen(self):
        self.chosen_piece = "Queen"
        self.accept()

    def choose_rook(self):
        self.chosen_piece = "Rook"
        self.accept()

    def choose_bishop(self):
        self.chosen_piece = "Bishop"
        self.accept()

    def choose_knight(self):
        self.chosen_piece = "Knight"
        self.accept()
