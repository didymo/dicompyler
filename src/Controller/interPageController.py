import sys
from PyQt5 import QtCore, QtWidgets
from src.View.mainPage import *
from src.View.openpage import WelcomePage
from src.Model.CalculateImages import *
from src.Model.LoadPatients import *


class Welcome(QtWidgets.QMainWindow, WelcomePage):
    open_patient_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.patientHandler)

    def patientHandler(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select patient folder...', '/home')
        self.open_patient_window.emit(path)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    open_patient_window = QtCore.pyqtSignal(str)

    def __init__(self, path, dataset, pixmaps):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self, path, dataset, pixmaps)

        self.actionOpen.triggered.connect(self.patientHandler)

    def patientHandler(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select patient folder...', '/home')
        self.open_patient_window.emit(path)


class Controller:

    def __init__(self):
        pass

    def show_welcome(self):
        self.welcome_window = Welcome()
        self.welcome_window.open_patient_window.connect(self.show_patient)
        self.welcome_window.show()

    def show_patient(self, path):
        dataset = get_datasets(path)
        pixmaps = get_pixmaps(dataset)

        window = QtWidgets.QMainWindow()
        self.patient_window = MainWindow(path, dataset, pixmaps)
        self.patient_window.open_patient_window.connect(self.show_patient)
        self.welcome_window.close()
        if self.patient_window.isVisible():
            self.patient_window.close()
        self.patient_window.show()
