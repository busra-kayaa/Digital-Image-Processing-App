import math
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QFileDialog, QMessageBox, QApplication
)
from PyQt5.QtGui import QPixmap, QImage

class RotateImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manuel Görüntü Döndürme")
        self.original_image = None
        self.processed_image = None
        self.total_angle = 0
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.image_label = QLabel("Görüntü Yüklenmedi")
        self.image_label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #444;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Dönme açısı (derece)")
        self.angle_input.setStyleSheet("font-size: 14pt; padding: 8px; border: 1px solid #aaa; border-radius: 10px;")
        self.layout.addWidget(self.angle_input)

        self.load_button = QPushButton("Görüntü Yükle")
        self.load_button.setStyleSheet(
            "background-color: #FF8C00; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.rotate_button = QPushButton("Döndür")
        self.rotate_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.rotate_button.clicked.connect(self.apply_rotation)
        self.layout.addWidget(self.rotate_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet(
            "background-color: #F44336; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.reset_button.clicked.connect(self.reset_image)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Görüntü Dosyaları (*.png *.jpg *.jpeg *.pgm)")
        if not path:
            return

        self.original_image = cv2.imread(path)
        self.processed_image = self.original_image.copy()
        self.total_angle = 0
        self.display_image(self.original_image)

    def display_image(self, img):
        if img is None:
            return

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img_rgb.shape
        bytes_per_line = 3 * width
        qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(600, 600, Qt.KeepAspectRatio)

        self.image_label.setPixmap(pixmap)
        self.image_label.setText("")
        self.image_label.setStyleSheet("")

    def apply_rotation(self):
        if self.original_image is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir görüntü yükleyin.")
            return

        try:
            angle = float(self.angle_input.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir açı girin.")
            return

        self.total_angle += angle
        rotated = self.rotate_image_manual(self.original_image, self.total_angle)
        self.processed_image = rotated
        self.display_image(rotated)

    def reset_image(self):
        if self.original_image is None:
            return
        self.total_angle = 0
        self.processed_image = self.original_image.copy()
        self.display_image(self.original_image)

    def rotate_image_manual(self, img, angle_deg):
        angle_rad = math.radians(angle_deg)
        h, w = img.shape[:2]

        # Yeni tuval boyutunu hesapla (görüntü köşeleri döndüğünde dışarı taşmayacak şekilde)
        new_w = int(abs(h * math.sin(angle_rad)) + abs(w * math.cos(angle_rad)))
        new_h = int(abs(h * math.cos(angle_rad)) + abs(w * math.sin(angle_rad)))

        canvas = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255  # Beyaz arka plan

        # Eski merkezin yeni merkeze göre konum farkı
        cx_old, cy_old = w / 2, h / 2
        cx_new, cy_new = new_w / 2, new_h / 2

        for y in range(new_h):
            for x in range(new_w):
                # Yeni koordinatları eski koordinat sistemine çevir
                xt = x - cx_new
                yt = y - cy_new

                # Koordinat dönüşümü
                src_x = xt * math.cos(-angle_rad) - yt * math.sin(-angle_rad) + cx_old
                src_y = xt * math.sin(-angle_rad) + yt * math.cos(-angle_rad) + cy_old

                # Kaynak koordinatları görüntü boyutları içinde mi?
                if 0 <= src_x < w and 0 <= src_y < h:
                    src_x = int(src_x)
                    src_y = int(src_y)
                    canvas[y, x] = img[src_y, src_x]

        return canvas

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RotateImage()
    window.show()
    sys.exit(app.exec_())
