from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class DeblurringPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Bir resim seçiniz")
        self.label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        layout.addWidget(self.label)

        self.btn_load = QPushButton("📂 Resim Yükle")
        self.btn_load.clicked.connect(self.load_image)
        self.btn_load.setStyleSheet("""
               QPushButton {
                   background-color: #3F51B5; color: white; font-size: 14pt; border-radius: 10px; padding: 10px;
               }
               QPushButton:hover {
                   background-color: #5C6BC0;
               }
           """)
        layout.addWidget(self.btn_load)

        self.btn_deblur = QPushButton("🌀 Deblur (Wiener Filter)")
        self.btn_deblur.clicked.connect(self.apply_deblurring)
        self.btn_deblur.setStyleSheet("""
               QPushButton {
                   background-color: #00BCD4; color: white; font-size: 14pt; border-radius: 10px; padding: 10px;
               }
               QPushButton:hover {
                   background-color: #26C6DA;
               }
           """)
        layout.addWidget(self.btn_deblur)

        self.btn_sharpen = QPushButton("🔍 Netleştir (Unsharp Masking)")
        self.btn_sharpen.clicked.connect(self.apply_unsharp_masking)
        self.btn_sharpen.setStyleSheet("""
               QPushButton {
                   background-color: #37474F; color: white; font-size: 14pt; border-radius: 10px; padding: 10px;
               }
               QPushButton:hover {
                   background-color: #455A64;
               }
           """)
        layout.addWidget(self.btn_sharpen)

        self.setLayout(layout)
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image = cv2.imread(path, cv2.IMREAD_COLOR)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # RGB'ye çevir
            self.show_image(self.image)

    def show_image(self, img):
        if len(img.shape) == 2:
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Grayscale8)
        else:
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def deblur_motion_blur(self, image, kernel_size=15, angle=0):
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
        kernel[kernel_size // 2, :] = np.ones(kernel_size, dtype=np.float32)

        M = cv2.getRotationMatrix2D((kernel_size // 2, kernel_size // 2), angle, 1)
        kernel = cv2.warpAffine(kernel, M, (kernel_size, kernel_size))
        kernel /= np.sum(kernel)

        if len(image.shape) == 2:
            deblurred = cv2.filter2D(image, -1, kernel)
            deblurred = cv2.equalizeHist(deblurred)
        else:
            channels = cv2.split(image)
            deblurred_channels = []
            for ch in channels:
                deb = cv2.filter2D(ch, -1, kernel)
                deb = cv2.equalizeHist(deb)
                deblurred_channels.append(deb)
            deblurred = cv2.merge(deblurred_channels)

        return deblurred

    def apply_deblurring(self):
        if hasattr(self, 'image'):
            h, w = self.image.shape[:2]
            kernel_size = max(3, int(min(h, w) * 0.02))
            if kernel_size % 2 == 0:
                kernel_size += 1
            angle = 0
            result = self.deblur_motion_blur(self.image, kernel_size, angle)
            self.show_image(result)

    def apply_unsharp_masking(self):
        if hasattr(self, 'image'):
            result = self.unsharp_mask(self.image)
            self.show_image(result)

    def unsharp_mask(self, image, kernel_size=(9, 9), sigma=10.0, amount=1.5, threshold=0):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
        return sharpened
