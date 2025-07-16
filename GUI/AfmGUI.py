# AfmGUI.py
import time, serial, os
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel
)


class AfmPageWidget(QWidget):

    back_requested = pyqtSignal()
    map_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("AfmPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        with open("Styles/styleAfmPage.qss", "r") as f:
            self.setStyleSheet(f.read())

        # ── CONFIG ────────────────────────────────
        self.PORT = "/dev/cu.usbmodem14101"
        self.BAUD = 115_200

        self.INIT_Y_MINMAX = (0, 0.5)
        self.AUTO_TRIP_DEG = 2.0
        self.SETTLE_DEG = 0.5
        self.SETTLE_SECS = 10.0
        self.WINDOW_SECONDS = 10
        self.TIMER_MS = 25

        self.DEAD_ZONE = 0.01
        self.LPF_ALPHA = 0.20

        self.MAX_TRIALS = 4
        self.RECORD_DURATION = 10
        self.MAX_VALUES_PER_TRIAL = 100
        self.TRIAL_FILE = "trials.txt"

        # ── Serial ────────────────────────────────
        self.init_serial()

        # ── GUI Setup ─────────────────────────────
        layout = QVBoxLayout(self)

        win = pg.GraphicsLayoutWidget(title="Gimbal angle (°)")
        layout.addWidget(win)

        self.plot = win.addPlot(labels={"left": "angle (°)", "bottom": "time (s)"})
        self.plot.setYRange(*self.INIT_Y_MINMAX, padding=0)
        self.plot.showGrid(x=True, y=True, alpha=0.3)

        orange_line = pg.InfiniteLine(pos=0.03, angle=0, pen=pg.mkPen("orange", width=2))
        self.plot.addItem(orange_line)
        self.curve = self.plot.plot(pen="y")

        self.record_button = QPushButton("Record")
        layout.addWidget(self.record_button)

        self.map_button = QPushButton("Map")
        layout.addWidget(self.map_button)

        self.clear_trial_file_button = QPushButton("Clear Trials")
        layout.addWidget(self.clear_trial_file_button)

        self.back_button = QPushButton("Back")
        layout.addWidget(self.back_button)

        self.trial_label = QLabel("Current Trial: 0 / 10")
        layout.addWidget(self.trial_label)

        self.trial_counter = QLabel("Awaiting start...")
        layout.addWidget(self.trial_counter)

        # ── State Variables ───────────────────────
        self.data_t, self.data_deg = [], []
        self.t0, self.deg_filt = None, 0.0
        self.auto_scaled, self.settle_start = False, None
        self.recording, self.recorded_trial_data, self.record_start_time = False, [], None
        self.trial_index = 0

        # ── Load Trials ───────────────────────────
        self.load_trials()

        # ── Button Hooks ──────────────────────────
        self.record_button.clicked.connect(self.start_recording)
        self.map_button.clicked.connect(self.show_topographic_map)
        self.clear_trial_file_button.clicked.connect(self.clear_trial_file)
        self.back_button.clicked.connect(self.go_back)

        # ── Timer ─────────────────────────────────
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.TIMER_MS)

    def init_serial(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
        self.ser = serial.Serial(self.PORT, self.BAUD, timeout=0)

    def load_trials(self):
        if os.path.exists(self.TRIAL_FILE):
            with open(self.TRIAL_FILE, "r") as f:
                lines = f.readlines()
            self.trial_index = 0 if len(lines) >= self.MAX_TRIALS else len(lines)
        else:
            with open(self.TRIAL_FILE, "w") as f:
                f.write("")
        self.trial_label.setText(f"Current Trial: {self.trial_index} / {self.MAX_TRIALS}")

    def update(self):
        latest = None
        while self.ser.in_waiting:
            try:
                latest = float(self.ser.readline())
            except ValueError:
                continue
        if latest is None:
            return

        latest = 0.0 if abs(latest) < self.DEAD_ZONE else latest
        self.deg_filt = (1 - self.LPF_ALPHA) * self.deg_filt + self.LPF_ALPHA * latest

        now = time.time()
        if self.t0 is None:
            self.t0 = now
        self.data_t.append(now - self.t0)
        self.data_deg.append(self.deg_filt)

        self.curve.setData(self.data_t, self.data_deg)
        self.plot.setXRange(max(0, self.data_t[-1] - self.WINDOW_SECONDS), self.data_t[-1], padding=0)
        self.trial_label.setText(f"Current Trial: {self.trial_index} / {self.MAX_TRIALS}")

        if self.recording:
            seconds = int(now - self.record_start_time)
            self.trial_counter.setText(f"Seconds left: {10 - seconds}")
            if len(self.recorded_trial_data) < self.MAX_VALUES_PER_TRIAL:
                self.recorded_trial_data.append(self.deg_filt)
            if now - self.record_start_time >= self.RECORD_DURATION:
                self.stop_recording()

    def start_recording(self):
        if self.trial_index >= self.MAX_TRIALS:
            return
        self.recording = True
        self.recorded_trial_data = []
        self.record_start_time = time.time()

    def stop_recording(self):
        self.recording = False
        with open(self.TRIAL_FILE, "a") as f:
            f.write(",".join(f"{v:.4f}" for v in self.recorded_trial_data) + "\n")
        self.trial_index += 1

    def clear_trial_file(self):
        with open(self.TRIAL_FILE, "w") as f:
            f.write("")
        self.trial_index = 0

    def show_topographic_map(self):
        if not os.path.exists(self.TRIAL_FILE): return
        with open(self.TRIAL_FILE) as f:
            lines = f.readlines()
        data = [list(map(float, line.strip().split(","))) for line in lines[:self.MAX_TRIALS]]
        plt.imshow(np.array(data), cmap="Greens", aspect="auto")
        plt.colorbar()
        plt.show()

    def go_back(self):
        self.timer.stop()
        self.back_requested.emit()

    def closeEvent(self, event):
        if self.ser and self.ser.is_open:
            self.ser.close()
        super().closeEvent(event)