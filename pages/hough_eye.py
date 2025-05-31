from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
import cv2
import os

class HoughEyePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Göz tespiti yapılacak resim burada gösterilecek.")
        self.label.setStyleSheet("font-size: 20pt; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Gözleri Tespit Et")
        self.button.setStyleSheet(
            "background-color: #28a745 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;"
        )
        self.button.clicked.connect(self.detect_eyes)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def detect_eyes(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "../images/yuz.jpg")

        print("Resim Yolu:", image_path)

        img = cv2.imread(image_path)
        if img is None:
            self.label.setText("Görüntü yüklenemedi.")
            return

        yuz = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        goz = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

        gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = yuz.detectMultiScale(gri, 1.3, 4)

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            img2 = img[y: y+h, x:x+w]
            gri2 = gri[y: y+h, x:x+w]

            gozler = goz.detectMultiScale(gri2)
            goz_kutulari = []

            for x1, y1, w1, h1 in gozler:
                if y1 < gri2.shape[0] // 2:  # Sadece üst yarıda yer alan gözleri kabul et
                    goz_kutulari.append((x1, y1, w1, h1))
                    cv2.rectangle(img2, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)

        self.display_image(img)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img).scaled(800, 600))
