# main.py  –  app entry point & page router
import sys
import pathlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from GUI.MainMenu    import MenuPage
from GUI.AfmGUI      import AfmPageWidget
from GUI.TopographyGUI import TopographyPageWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Demo Kit")
        self.resize(800, 480)

        # ── stacked‑page container ──────────────────────────────────
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # page 0 → main menu
        self.menu_page = MenuPage()
        self.stack.addWidget(self.menu_page)
        

        # page 1 → AFM live‑plot
        self.afm_page = AfmPageWidget()
        self.stack.addWidget(self.afm_page)

        # ── navigation wiring ───────────────────────────────────────
        self.menu_page.afm_btn.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.afm_page)
        )
        self.afm_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.menu_page)
        )

        # page 2 → Topography page
        self.topo_page = TopographyPageWidget()
        self.stack.addWidget(self.topo_page)

        # connect AfmPageWidget to TopographyPageWidget
        self.afm_page.map_requested.connect(
            lambda: self.stack.setCurrentWidget(self.topo_page)
        )

        # Topography back to AfmPageWidget
        self.topo_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.afm_page)
        )

        # start on the menu
        self.stack.setCurrentWidget(self.menu_page)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
