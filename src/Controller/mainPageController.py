from src.View.mainPage import *


from src.Model.CalculateImages import *
from src.Model.LoadPatients import *


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        path = 'dicom_sample'
        dataset = get_datasets(path)
        pixmaps = get_pixmaps(dataset)

        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, pixmaps, path)

