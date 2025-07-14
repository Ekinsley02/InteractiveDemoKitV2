# main.py
# This code was writen by: Elliott Kinsley
# The purpose of this code is to create a GUI for an interactive demostration kit
# This mainn file is used to control GUI applications

# import libraries
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# global config variables

# build main application

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 800, 480)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: #655A7C;")

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # ────── 1) LOGO AT THE TOP ──────
        logo_lbl = QLabel()
        pixmap   = QPixmap("logo.png")                  # put your filename here
        # If you want to guarantee it fits:
        pixmap   = pixmap.scaledToWidth(
            250, Qt.TransformationMode.SmoothTransformation
        )
        logo_lbl.setPixmap(pixmap)
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(logo_lbl)
        # add label
        self.introLabel = QLabel("Welcome to the interactive demostration kit!")
        self.introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.introLabel)

        # Add buttons
        self.afmButton = QPushButton("Atomic Force Microscope")
        self.layout.addWidget(self.afmButton)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
