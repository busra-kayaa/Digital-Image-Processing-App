import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QFileDialog, QMessageBox, QScrollArea)
from PyQt5.QtGui import QPixmap, QImage


class ZoomPage(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.processed_image = None
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

        # Zoom işlemi için giriş alanı
        self.zoom_input = QLineEdit()
        self.zoom_input.setPlaceholderText("Zoom faktörü (örn: 1.5 veya 0.5)")
        self.zoom_input.setStyleSheet("""
            font-size: 14pt; 
            padding: 8px; 
            border: 1px solid #aaa;
            border-radius: 10px;
            background-color: #F8F9FA;
        """)
        layout.addWidget(self.zoom_input)

        # Zoom butonları
        self.zoom_in_button = QPushButton(" Zoom In (Büyüt)")
        self.zoom_out_button = QPushButton(" Zoom Out (Küçült)")

        # Buton stilleri
        self.zoom_in_button.setStyleSheet("""
            QPushButton {
                background-color: #107bff;
                color: white;
                font-size: 14pt;
                padding: 10px;
                border-radius: 10px;
                min-width: 200px;
                border: 2px;
            }
        """)

        self.zoom_out_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5722;
                color: white;
                font-size: 14pt;
                padding: 10px;
                border-radius: 10px;
                min-width: 200px;
                border: 2px;
            }
        """)

        self.zoom_in_button.clicked.connect(self.handle_zoom)
        self.zoom_out_button.clicked.connect(self.handle_zoom)

        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)

        # Görüntü yükleme butonu
        self.load_button = QPushButton(" Görüntü Yükle")
        self.load_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 14pt;
                padding: 10px;
                border-radius: 8px;
                border: 2px;
            }
        """)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    # ... (load_image, display_image, handle_zoom ve zoom_image fonksiyonları öncekiyle aynı)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Görüntü Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return

        self.image = cv2.imread(path)
        if self.image is None:
            QMessageBox.critical(self, "Hata", "Görüntü yüklenemedi!")
            return

        self.processed_image = self.image.copy()
        self.display_image(self.image)

    def display_image(self, img):
        if img is None:
            return

        h, w = img.shape[:2]
        bytes_per_line = 3 * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def handle_zoom(self):
        # Temel kontroller
        if self.image is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return

        factor_text = self.zoom_input.text().strip()
        if not factor_text:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir zoom faktörü girin!")
            return

        try:
            factor = float(factor_text)
            if factor <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçersiz zoom değeri! Pozitif sayı girin.")
            return

        # Hangi butona tıklandığını belirle
        sender = self.sender()
        try:
            if sender == self.zoom_in_button:
                self.processed_image = self.zoom_image(self.processed_image, factor)
            elif sender == self.zoom_out_button:
                self.processed_image = self.zoom_image(self.processed_image, 1 / factor)

            self.display_image(self.processed_image)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Zoom hatası: {str(e)}")

    def zoom_image(self, img, factor):
        if img is None:
            raise ValueError("Görüntü bulunamadı!")

        h, w = img.shape[:2]
        new_size = (int(w * factor), int(h * factor))

        if new_size[0] == 0 or new_size[1] == 0:
            raise ValueError("Zoom değeri çok küçük!")

        return cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)