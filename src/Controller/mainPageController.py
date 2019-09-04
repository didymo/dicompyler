from src.View.mainPage import *


from src.Model.CalculateImages import *
from src.Model.LoadPatients import *


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        self.path = 'dicom_sample'
        self.dataset = get_datasets(self.path)
        self.pixmaps = get_pixmaps(self.dataset)


    def displayMainPage(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self.pixmaps, self.path)

