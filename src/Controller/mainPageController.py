from src.View.mainPage import *


from src.Model.CalculateImages import *
from src.Model.LoadPatients import *
from src.Model.Pyradiomics import pyradiomics
from PyQt5 import QtWidgets



class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        self.path = ''
        self.dataset = []
        self.pixmaps = []


    def displayMainPage(self):
        QtWidgets.QWidget.__init__(self)
        print(self.path)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self.pixmaps, self.path)

    def openPatient(self):
        self.path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select patient folder...')
        self.dataset = get_datasets(self.path)
        self.pixmaps = get_pixmaps(self.dataset)
        self.displayMainPage()
        self.show()

    def runPyradiomics(self, dirPath):
        pyradiomics(dirPath)
