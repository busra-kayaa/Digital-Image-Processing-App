from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

def normalize_image(img):
    return img.astype(np.float32) / 255.0

def denormalize_image(img):
    return np.clip(img * 255, 0, 255).astype(np.uint8)

def standard_sigmoid(x):
    return 1 / (1 + np.exp(-10 * (x - 0.5)))

def shifted_sigmoid(x):
    return 1 / (1 + np.exp(-10 * (x - 0.3)))

def sloped_sigmoid(x):
    return 1 / (1 + np.exp(-20 * (x - 0.5)))

def custom_function(x):
    return np.tanh(5.5 * (x - 0.5)) * 0.5 + 0.5

class SCurvePage(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.original_image = None

        layout = QVBoxLayout()
        self.label = QLabel("Görüntü Yüklenmedi")
        self.label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()

        load_btn = QPushButton("Görüntü Yükle")
        load_btn.setStyleSheet("background-color: #2E8B57 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        load_btn.clicked.connect(self.load_image)
        btn_layout.addWidget(load_btn)

        btns = [
            ("Standart Sigmoid", standard_sigmoid),
            ("Kaydırılmış Sigmoid", shifted_sigmoid),
            ("Eğimli Sigmoid", sloped_sigmoid),
            ("Özel Fonksiyon", custom_function)
        ]

        button_style = """
            background-color: #D72638;
            color: white;
            font-size: 14pt;
            padding: 10px;
            border-radius: 10px;
        """

        for name, func in btns:
            btn = QPushButton(name)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda _, f=func: self.apply_and_show(f))
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.image = self.original_image.copy()
            self.show_image(self.image)

    def apply_and_show(self, func):
        if self.original_image is not None:
            norm_img = normalize_image(self.original_image)
            transformed = func(norm_img)
            result = denormalize_image(transformed)
            self.image = result
            self.show_image(result)

    def show_image(self, img):
        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg).scaled(512, 512, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
