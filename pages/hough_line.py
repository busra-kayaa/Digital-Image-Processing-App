from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import os

class HoughLinePage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("Çizgi tespiti yapılacak resim burada gösterilecek.")
        self.label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Resimde Çizgileri Tespit Et")
        self.button.setStyleSheet(
            "background-color: #28a745 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.button.clicked.connect(self.detect_lines)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def detect_lines(self):
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images/line.png")
        image = cv2.imread(image_path)

        if image is None:
            self.label.setText("Resim yüklenemedi. Yol: " + image_path)
            return

        image = cv2.resize(image, (800, 600))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kenar = cv2.Canny(gray, 50, 150)
        cizgi = cv2.HoughLinesP(kenar, 1, np.pi / 180, threshold=30, minLineLength=50, maxLineGap=10)

        if cizgi is not None:
            for i in cizgi:
                x1, y1, x2, y2 = i[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        else:
            self.label.setText("Çizgi bulunamadı.")

        self.display_image(image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img).scaled(800, 600))
