from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
import pandas as pd
from skimage.measure import regionprops, label
import os

class ObjectDetectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = os.path.join(os.path.dirname(__file__), "../images/nesne.jpg")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Yüklü görüntü")
        self.label.setScaledContents(True)
        layout.addWidget(self.label)

        self.btn_process = QPushButton("Koyu Yeşil Nesne Analizi")

        button_style = """
        QPushButton {
            background-color: #2E7D32;
            color: white;
            font-size: 14pt;
            padding: 10px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #388E3C;
        }
        """

        self.btn_process.setStyleSheet(button_style)

        self.btn_process.clicked.connect(self.process_image)
        layout.addWidget(self.btn_process)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.load_image()

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        if self.image is not None:
            rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            qimg = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qimg))

    def process_image(self):
        if self.image is None:
            return

        # HSV dönüşüm ve koyu yeşil maske
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 100, 50])
        upper_green = np.array([80, 255, 200])  # üst sınır düşürüldü: sadece koyu yeşil

        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Gürültü temizliği
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)

        # İşlenmiş görüntü oluştur
        masked_img = cv2.bitwise_and(self.image, self.image, mask=mask)

        # Görüntüyü kaydet
        output_img_path = os.path.join(os.path.dirname(__file__), "../output/koyu_yesil_sonuclu.png")
        cv2.imwrite(output_img_path, masked_img)

        # Label işlemleri ve analiz
        labeled = label(mask)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        props = regionprops(labeled, intensity_image=gray)

        results = []
        for i, region in enumerate(props, 1):
            y, x = region.centroid
            minr, minc, maxr, maxc = region.bbox
            length = maxr - minr
            width = maxc - minc
            diagonal = int(np.sqrt(length ** 2 + width ** 2))
            intensity = region.intensity_image

            energy = np.sum(intensity ** 2)
            hist, _ = np.histogram(intensity, bins=256, range=(0, 256), density=True)
            entropy = -np.sum(hist * np.log2(hist + 1e-8))
            mean = int(np.mean(intensity))
            median = int(np.median(intensity))

            results.append({
                "No": i,
                "Center": f"{int(x)},{int(y)}",
                "Length": f"{length} px",
                "Width": f"{width} px",
                "Diagonal": f"{diagonal} px",
                "Energy": round(energy / 1000, 3),
                "Entropy": round(entropy, 2),
                "Mean": mean,
                "Median": median
            })

        # DataFrame oluştur ve göster
        df = pd.DataFrame(results)
        self.text_edit.setText(df.to_string(index=False))

        # Tabloyu CSV olarak kaydet
        output_csv_path = os.path.join(os.path.dirname(__file__), "../output/koyu_yesil_analiz.csv")
        df.to_csv(output_csv_path, index=False)

        # Görüntüyü göster
        cv2.imshow("Koyu Yesil Nesneler", masked_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
