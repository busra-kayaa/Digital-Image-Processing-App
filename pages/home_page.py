# pages/home_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

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

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        home_label = QLabel("📷 Ders: Dijital Görüntü İşleme\n\n\n👩‍🎓 Öğrenci No: 221229007\n📌 Ad Soyad: Büşra KAYA",self)
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
