from src.View.mainPage import *
from src.Model.LoadPatients import *
from src.Model.CalculateImages import *


class MainPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        path = 'dicom_sample'
        dataset = get_datasets(path)
        img_dict = get_img(dataset)

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, img_dict)