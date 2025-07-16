import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

TRIAL_FILE = "trials.txt"
MAX_VALUES_PER_TRIAL = 100
MAX_TRIALS = 4

class TopographyPageWidget(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        title = QLabel("Topographic Map")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # pyqtgraph canvas
        self.graph = pg.GraphicsLayoutWidget()
        layout.addWidget(self.graph, stretch=1)

        self.plot = self.graph.addPlot()
        self.img_item = pg.ImageItem()
        self.plot.addItem(self.img_item)
        self.plot.setLabel('left', "Trial Layer (Top to Bottom)")
        self.plot.setLabel('bottom', "Position (left to right)")
        self.plot.invertY(True)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.back_requested.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.load_data()

    def load_data(self):
        try:
            with open(TRIAL_FILE, "r") as f:
                lines = f.readlines()
            data = []
            for line in lines[:MAX_TRIALS]:
                row = [float(v) for v in line.strip().split(",")[:MAX_VALUES_PER_TRIAL]]
                if len(row) < MAX_VALUES_PER_TRIAL:
                    row += [0.0] * (MAX_VALUES_PER_TRIAL - len(row))
                data.append(row)
            array = np.array(data)
            norm_array = np.clip(array / 1.5, 0, 1)
            self.img_item.setImage(norm_array, cmap='viridis')
            
        except Exception as e:
            print(f"Error loading data: {e}")
