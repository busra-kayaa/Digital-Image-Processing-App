import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QMessageBox

from pages.home_page import HomePage
from pages.odev1_page1 import Odev1Page
from pages.odev1_page2 import Odev1Page2
from pages.odev2_page1 import ResizePage
from pages.odev2_page2 import ZoomPage
from  pages.odev2_page3 import RotateImage
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
        self.tab_widget.addTab(Odev1Page(), "Temel İşlevsellik")
        self.tab_widget.addTab(Odev1Page2(), "Filtre Uygulama")
        self.tab_widget.addTab(ResizePage(), "Boyut Değiştir (Büyüt/Küçült)")
        self.tab_widget.addTab(ZoomPage(), "Yakınlaştır / Uzaklaştır ")
        self.tab_widget.addTab(RotateImage(), "Döndürme")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())