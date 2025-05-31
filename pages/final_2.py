from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from pages.hough_line import HoughLinePage
from pages.hough_eye import HoughEyePage

class HoughTransformPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        tabs = QTabWidget()

        tabs.addTab(HoughLinePage(), "Çizgi Tespiti")
        tabs.addTab(HoughEyePage(), "Göz Tespiti")

        layout.addWidget(tabs)
        self.setLayout(layout)
