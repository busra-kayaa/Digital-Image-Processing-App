import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QAction, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QDialog, QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import matplotlib.pyplot as plt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        home_label = QLabel("📷 Ders: Dijital Görüntü İşleme\n\n\n👩‍🎓 Öğrenci No: 221229007\n📌 Ad Soyad: Büşra KAYA", self)
        home_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: #333;
            text-align: center;
        """)
        home_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(home_label)
        self.setLayout(layout)

        about_button = QPushButton("ℹ️ Hakkında")
        about_button.setStyleSheet("""
            QPushButton {
                background-color: #1e88e5;
                color: white;
                font-size: 14pt;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        about_button.clicked.connect(self.show_about)
        layout.addWidget(about_button)

    def show_about(self):
        QMessageBox.information(self, "Hakkında", "Bu uygulama Dijital Görüntü İşleme dersi için hazırlanmıştır.")
class Odev1Page(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None

        layout = QVBoxLayout(self)
        self.image_label = QLabel("Resim Yüklenmedi")
        self.image_label.setStyleSheet("font-size: 22pt; font-weight: bold; color: #333;")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_image_button = QPushButton("Resim Yükle")
        self.load_image_button.setStyleSheet(
            "background-color: #32CD32 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.load_image_button.clicked.connect(self.load_image)

        self.load_histogram_button = QPushButton("Histogram Oluştur")
        self.load_histogram_button.setStyleSheet(
            "background-color: #FF8C00 ; color: white; font-size: 14pt; padding: 10px; border-radius: 10px;")
        self.load_histogram_button.clicked.connect(self.load_histogram)

        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.load_histogram_button)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.png)")
        if file_path:
            pixmap = QPixmap(file_path).scaled(800, 600, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image = cv2.imread(file_path)

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

class Odev2Page(QWidget):
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
            file_path, file_type = QFileDialog.getSaveFileName(self, "Filtreli Görüntüyü Kaydet", "filtered_image.png",
                                                               "Görüntü Dosyaları (*.png *.jpg *.bmp *.jpeg);;PNG Dosyaları (*.png);;JPEG Dosyaları (*.jpg *.jpeg);;BMP Dosyaları (*.bmp)")
            if file_path:
                if file_type == "PNG Dosyaları (*.png)" or file_type == "Görüntü Dosyaları (*.png)":
                    cv2.imwrite(file_path, self.image)
                    QMessageBox.information(self, "Bilgi", "Filtreli görüntü başarıyla PNG formatında kaydedildi.")
                elif file_type == "JPEG Dosyaları (*.jpg *.jpeg)":
                    cv2.imwrite(file_path, self.image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                    QMessageBox.information(self, "Bilgi", "Filtreli görüntü başarıyla JPEG formatında kaydedildi.")
                elif file_type == "BMP Dosyaları (*.bmp)":
                    cv2.imwrite(file_path, self.image)
                    QMessageBox.information(self, "Bilgi", "Filtreli görüntü başarıyla BMP formatında kaydedildi.")
                else:
                    cv2.imwrite(file_path, self.image)
                    QMessageBox.information(self, "Bilgi", "Filtreli görüntü başarıyla PNG formatında kaydedildi.")
            else:
                QMessageBox.warning(self, "Uyarı", "Dosya kaydedilmedi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir filtre uygulayın.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dijital Görüntü İşleme Uygulaması")
        self.setGeometry(100, 100, 1200, 800)

        self.menu_bar = self.menuBar()
        self.create_menu()
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.create_tabs()

    def create_menu(self):
        file_menu = self.menu_bar.addMenu("Dosya")
        exit_action = QAction("Çıkış", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = self.menu_bar.addMenu("Yardım")
        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(
            lambda: QMessageBox.information(self, "Hakkında", "Dijital Görüntü İşleme Uygulaması v1.0"))
        help_menu.addAction(about_action)

    def create_tabs(self):
        self.tab_widget.addTab(HomePage(), "Ana Sayfa")
        self.tab_widget.addTab(Odev1Page(), "Temel İşlevselliği Oluştur")
        self.tab_widget.addTab(Odev2Page(), "Filtre Uygulama")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())