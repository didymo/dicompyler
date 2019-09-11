from src.View.mainPage import *


from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from src.Model.GetPatientInfo import *


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        path = 'dicom_sample'

        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, path)

