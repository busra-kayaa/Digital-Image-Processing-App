import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from matplotlib import pyplot as plt


class Odev1Page(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.processed_image = None

        layout = QVBoxLayout(self)

        self.image_label = QLabel("Resim Yüklenmedi")
        self.image_label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #333;")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_image_button = QPushButton("Resim Yükle")
        self.load_image_button.setStyleSheet(
            "background-color: #32CD32 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.load_image_button.clicked.connect(self.load_image)

        self.grayscale_button = QPushButton("Gri Tonlamaya Çevir")
        self.grayscale_button.setStyleSheet(
            "background-color: #007bff; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)

        self.save_button = QPushButton("Gri Tonlamalı Resmi Kaydet")
        self.save_button.setStyleSheet(
            "background-color: #dc3545; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.save_button.clicked.connect(self.save_image)

        self.load_histogram_button = QPushButton("Histogram Oluştur")
        self.load_histogram_button.setStyleSheet(
            "background-color: #FF8C00 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.load_histogram_button.clicked.connect(self.load_histogram)

        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.grayscale_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_histogram_button)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.png)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.processed_image = self.image.copy()
            self.display_image(self.image)

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(800, 600, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def convert_to_grayscale(self):
        if self.image is not None:
            self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2RGB)
            self.display_image(self.processed_image)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim yükleyin.")

    def save_image(self):
        if self.processed_image is not None:
            default_path = "grayscale_image.png"
            file_path, _ = QFileDialog.getSaveFileName(self, "Gri Tonlamalı Resmi Kaydet", default_path, "PNG Dosyaları (*.png);;JPEG Dosyaları (*.jpg)")
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))
                QMessageBox.information(self, "Bilgi", "Gri tonlamalı resim başarıyla kaydedildi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resmi gri tonlamaya çevirin.")

    def load_histogram(self):
        if self.image is not None:
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv2.calcHist([self.image], [i], None, [256], [0, 256])
                plt.plot(hist, color=col)
            plt.title("RGB Histogram")
            plt.xlabel("Pixel Değerleri")
            plt.ylabel("Frekans")
            plt.show()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim yükleyin.")
