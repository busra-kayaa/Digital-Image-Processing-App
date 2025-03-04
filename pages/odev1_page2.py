import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QLabel, QWidget, QVBoxLayout, QPushButton, QRadioButton, QMessageBox, \
    QButtonGroup, QDialog

class Odev1Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None

        layout = QVBoxLayout(self)
        self.filtered_image_label = QLabel("Filtre Uygulanmadı")
        self.filtered_image_label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #333;")
        self.filtered_image_label.setAlignment(Qt.AlignCenter)

        self.apply_filter_button = QPushButton("Filtre Uygula")
        self.apply_filter_button.setStyleSheet("background-color: #8000FF ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.apply_filter_button.clicked.connect(self.apply_filter)

        self.save_filtered_button = QPushButton("Filtreli Görüntüyü Kaydet")
        self.save_filtered_button.setStyleSheet("background-color: #FF1493 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.save_filtered_button.clicked.connect(self.save_filtered_image)

        layout.addWidget(self.filtered_image_label)
        layout.addWidget(self.apply_filter_button)
        layout.addWidget(self.save_filtered_button)

    def apply_filter(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.png)")
        if file_path:
            self.image = cv2.imread(file_path)
            filter_type, ok = self.choose_filter()
            if ok:
                self.image = self.apply_selected_filter(filter_type)
                self.display_image(self.image)

    def choose_filter(self):
        filters = {"Gaussian": 0, "Median": 1, "Canny": 2, "Sobel": 3}
        dialog = QDialog(self)
        dialog.setWindowTitle("Filtre Seçiniz")
        dialog.setWindowFlag(Qt.FramelessWindowHint, False)
        dialog.setFixedSize(200, 150)
        layout = QVBoxLayout(dialog)
        button_group = QButtonGroup(dialog)
        buttons = []

        for key in filters:
            btn = QRadioButton(key)
            button_group.addButton(btn, filters[key])
            buttons.append(btn)
            layout.addWidget(btn)

        apply_button = QPushButton("Uygula")
        apply_button.setStyleSheet("background-color: #D81B60; color: white;")
        apply_button.clicked.connect(dialog.accept)
        layout.addWidget(apply_button)

        if dialog.exec_():
            selected = button_group.checkedId()
            return list(filters.keys())[selected], True
        return None, False

    def apply_selected_filter(self, filter_type):
        if filter_type == "Gaussian":
            return cv2.GaussianBlur(self.image, (15, 15), 0)
        elif filter_type == "Median":
            return cv2.medianBlur(self.image, 15)
        elif filter_type == "Canny":
            return cv2.Canny(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), 100, 200)
        elif filter_type == "Sobel":
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            return cv2.convertScaleAbs(cv2.magnitude(grad_x, grad_y))

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], img_rgb.strides[0], QImage.Format_RGB888)
        self.filtered_image_label.setPixmap(QPixmap.fromImage(qimg))

    def save_filtered_image(self):
        if self.image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Filtreli Görüntüyü Kaydet", "filtered_image.png",
                "PNG Dosyaları (*.png);;JPEG Dosyaları (*.jpg *.jpeg);;BMP Dosyaları (*.bmp);;Tüm Dosyalar (*.*)"
            )

            if file_path:
                file_extension = file_path.split('.')[-1].lower()

                if file_extension not in ["png", "jpg", "jpeg", "bmp"]:
                    file_path += ".png"
                    file_extension = "png"

                params = []
                if file_extension in ["jpg", "jpeg"]:
                    params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

                cv2.imwrite(file_path, self.image, params)
                QMessageBox.information(self, "Bilgi",
                                        f"Filtreli görüntü başarıyla {file_extension.upper()} formatında kaydedildi.")
            else:
                QMessageBox.warning(self, "Uyarı", "Dosya kaydedilmedi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir filtre uygulayın.")
