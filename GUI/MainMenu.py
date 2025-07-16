# menu_page.py  (new file, or inline class)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QPixmap

class MenuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("CentralArea")                      
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        with open("Styles/styleMainPage.qss", "r") as f:
                    self.setStyleSheet(f.read())

        lay = QVBoxLayout(self)
        lay.setSpacing(16)

        # logo
        logo_lbl = QLabel()
        logo_lbl.setPixmap(
            QPixmap("images/logo.png")
            .scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
        )
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(logo_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

        # headline banner
        headline = QLabel("Welcome to the Interactive Demo Kit!")
        headline.setObjectName("IntroLabel")
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(headline, alignment=Qt.AlignmentFlag.AlignHCenter)

        lay.addSpacing(12) 

        # primary button → AFM page
        self.afm_btn = QPushButton("Atomic Force Microscope")
        self.afm_btn.setObjectName("AfmBtn")
        lay.addWidget(self.afm_btn, alignment=Qt.AlignmentFlag.AlignHCenter)


        lay.addStretch()    

