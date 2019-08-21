from PyQt5.QtWidgets import QMainWindow, QLabel, QSizePolicy, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import numpy as np
import sys

import pydicom

# QImage is designed and optimized for I/O,
# and for direct pixel access and manipulation,
# while QPixmap is designed and optimized for showing images on screen.
# path = '/home/xudong/dicom_sample'


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 10, 512, 512)

        pixmap_label = QLabel()
        pixmap_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        pixmap_label.setAlignment(Qt.AlignCenter)

        path = '/home/xudong/dicom_sample'
        filename = path + "/ct.100.dcm"
        ds = pydicom.dcmread(filename)
        ds.convert_pixel_data()
        np_pixel = ds._pixel_array

        max = np.amax(np_pixel)
        min = np.amin(np_pixel)
        data = (np_pixel - min) / (max - min) * 256
        data[data < 0] = 0
        data[data > 255] = 255
        data = data.astype("int8")

        qimage = QImage(data, data.shape[1], data.shape[0],
                        QImage.Format_Indexed8)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(1024, 1024, Qt.KeepAspectRatio)
        pixmap_label.setPixmap(pixmap)

        self.setCentralWidget(pixmap_label)
        self.show()


def main():
    app = QApplication(sys.argv)
    win = Test()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
