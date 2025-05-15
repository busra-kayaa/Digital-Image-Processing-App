import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QFileDialog, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class ResizePage(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Scroll alanı ve görsel etiketi
        self.scroll_area = QScrollArea()
        self.label = QLabel("Görsel Yüklenmedi")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16pt; color: #888; border: 2px dashed #aaa;")
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.scale_input = QLineEdit()
        self.scale_input.setPlaceholderText("Ölçek faktörü (0.5, 2.0 vb.)")
        self.scale_input.setStyleSheet("font-size: 14pt; padding: 8px; border: 1px solid #aaa; border-radius: 10px;")
        layout.addWidget(self.scale_input)

        self.method_combo = QComboBox()
        self.method_combo.addItems(["Nearest", "Bilinear", "Average"])
        self.method_combo.setStyleSheet("font-size: 14pt; padding: 8px; border: 1px solid #aaa; border-radius: 10px;")
        layout.addWidget(self.method_combo)

        self.load_button = QPushButton("Görsel Yükle")
        self.load_button.setStyleSheet(
            "background-color: #3b82f6 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.resize_button = QPushButton("Boyut Değiştir")
        self.resize_button.setStyleSheet(
            "background-color: #ef4444; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.resize_button.clicked.connect(self.resize_image)
        layout.addWidget(self.resize_button)

        self.setLayout(layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Görüntü Dosyaları (*.pgm *.png *.jpg *.jpeg)")
        if path:
            img = Image.open(path).convert('RGB')  # Renkli yükle
            self.image = np.array(img)
            self.show_image(self.image)

    def show_image(self, img_array):
        height, width, channels = img_array.shape
        bytes_per_line = 3 * width
        qimg = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        self.label.setText("")
        self.label.setStyleSheet("border: none;")

    def resize_image(self):
        if self.image is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir görüntü yükleyin.")
            return

        try:
            factor = float(self.scale_input.text())
            if factor <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir pozitif sayı girin.")
            return

        new_h = int(self.image.shape[0] * factor)
        new_w = int(self.image.shape[1] * factor)

        method = self.method_combo.currentText()
        if method == "Bilinear":
            resized = self.bilinear_resize(self.image, new_w, new_h)
        elif method == "Nearest":
            resized = self.nearest_resize(self.image, new_w, new_h)
        elif method == "Average":
            resized = self.average_resize(self.image, new_w, new_h)
        else:
            QMessageBox.warning(self, "Uyarı", "Geçersiz yöntem.")
            return

        self.image = resized
        self.show_image(self.image)

    def nearest_resize(self, img_array, new_w, new_h):
        old_h, old_w = img_array.shape[:2]
        result = np.zeros((new_h, new_w, 3), dtype=np.uint8)
        for i in range(new_h):
            for j in range(new_w):
                y = int(i * old_h / new_h)
                x = int(j * old_w / new_w)
                result[i, j] = img_array[y, x]
        return result

    def bilinear_resize(self, img_array, new_w, new_h):
        old_h, old_w = img_array.shape[:2]
        result = np.zeros((new_h, new_w, 3), dtype=np.uint8)
        for i in range(new_h):
            for j in range(new_w):
                x = j * (old_w - 1) / (new_w - 1)
                y = i * (old_h - 1) / (new_h - 1)
                x0 = int(x)
                x1 = min(x0 + 1, old_w - 1)
                y0 = int(y)
                y1 = min(y0 + 1, old_h - 1)
                a = x - x0
                b = y - y0
                for c in range(3):
                    result[i, j, c] = int(
                        (1 - a) * (1 - b) * img_array[y0, x0, c] +
                        a * (1 - b) * img_array[y0, x1, c] +
                        (1 - a) * b * img_array[y1, x0, c] +
                        a * b * img_array[y1, x1, c]
                    )
        return result

    def average_resize(self, img_array, new_w, new_h):
        old_h, old_w = img_array.shape[:2]
        result = np.zeros((new_h, new_w, 3), dtype=np.uint8)
        x_ratio = old_w / new_w
        y_ratio = old_h / new_h

        for i in range(new_h):
            for j in range(new_w):
                x_start = int(j * x_ratio)
                x_end = min(int((j + 1) * x_ratio), old_w)
                y_start = int(i * y_ratio)
                y_end = min(int((i + 1) * y_ratio), old_h)
                block = img_array[y_start:y_end, x_start:x_end, :]
                avg = np.mean(block, axis=(0, 1))
                result[i, j] = avg.astype(np.uint8)
        return result
